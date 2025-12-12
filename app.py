from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import json
import os
import uuid

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'greyskull-workout-secret'

# File paths
EXERCISES_FILE = 'exercises.json'
WORKOUTS_FILE = 'workouts.json'

# Default exercises
DEFAULT_EXERCISES = {
    'ohp': {'name': 'Overhead Press / Bench Press', 'target_reps': 5},
    'rows': {'name': 'Chinups / Barbell Rows', 'target_reps': 5},
    'squats': {'name': 'Squats', 'target_reps': 5},
    'deadlifts': {'name': 'Deadlifts', 'target_reps': 1}
}

def load_exercises():
    """Load exercises from JSON file"""
    if os.path.exists(EXERCISES_FILE):
        with open(EXERCISES_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_EXERCISES

def save_exercises(exercises):
    """Save exercises to JSON file"""
    with open(EXERCISES_FILE, 'w') as f:
        json.dump(exercises, f, indent=2)

def load_workouts():
    """Load workouts from JSON file"""
    if os.path.exists(WORKOUTS_FILE):
        with open(WORKOUTS_FILE, 'r') as f:
            return json.load(f)
    return []


def is_mobile_request(req):
    """Rudimentary mobile detection based on User-Agent header"""
    ua = (req.headers.get('User-Agent') or '').lower()
    return 'mobile' in ua or 'iphone' in ua or 'android' in ua

def save_workouts(workouts):
    """Save workouts to JSON file"""
    with open(WORKOUTS_FILE, 'w') as f:
        json.dump(workouts, f, indent=2)

def get_last_workout(exercise_id):
    """Get the last workout for a specific exercise"""
    workouts = load_workouts()
    for workout in reversed(workouts):
        if workout['exercise_id'] == exercise_id:
            return workout
    return None

def calculate_next_weight(current_weight, reps_category):
    """Calculate recommended next weight based on reps performed"""
    if reps_category == 'more_than_10':
        # Hit AMRAP with 10+ reps, increase weight by 2.5kg
        return round(current_weight + 2.5, 1)
    elif reps_category == 'more_than_5':
        # Hit 5+ reps, increase weight by 1.5kg
        return round(current_weight + 1.5, 1)
    elif reps_category == 'less_than_5':
        # Didn't hit 5 reps, keep same weight
        return round(current_weight - current_weight * 0.10, 1)
    return current_weight

@app.route('/')
def index():
    """Index: list exercises"""
    exercises = load_exercises()
    # Build list with last workout info
    exercises_with_history = []
    for ex_id, ex in exercises.items():
        last = get_last_workout(ex_id)
        exercises_with_history.append({
            'id': ex_id,
            'name': ex['name'],
            'target_reps': ex['target_reps'],
            'last': last
        })
    # Serve a simplified mobile view when appropriate
    if is_mobile_request(request):
        return render_template('index_mobile.html', exercises=exercises_with_history)
    return render_template('index.html', exercises=exercises_with_history)

@app.route('/api/exercises')
def get_exercises():
    """Get all exercises with their last workout info"""
    exercises = load_exercises()
    exercises_with_history = []
    
    for ex_id, exercise in exercises.items():
        last = get_last_workout(ex_id)
        
        data = {
            'id': ex_id,
            'name': exercise['name'],
            'target_reps': exercise['target_reps'],
            'last_weight': None,
            'last_date': None,
            'next_suggested_weight': None
        }
        
        if last:
            data['last_weight'] = last['weight']
            data['last_date'] = last['date']
            data['next_suggested_weight'] = last['next_weight']
        
        exercises_with_history.append(data)
    
    return jsonify(exercises_with_history)


@app.route('/exercises/add', methods=['POST'])
def web_add_exercise():
    name = request.form.get('name', '').strip()
    try:
        target_reps = int(request.form.get('target_reps', 5))
    except ValueError:
        target_reps = 5

    if not name:
        flash('Exercise name required', 'danger')
        return redirect(url_for('index'))

    exercises = load_exercises()
    exercise_id = str(uuid.uuid4())[:8]
    exercises[exercise_id] = {'name': name, 'target_reps': target_reps}
    save_exercises(exercises)
    flash('Exercise added', 'success')
    return redirect(url_for('index'))

@app.route('/api/exercises', methods=['POST'])
def add_exercise():
    """Add a new exercise"""
    data = request.json
    name = data.get('name', '').strip()
    target_reps = int(data.get('target_reps', 5))
    
    if not name:
        return {'error': 'Exercise name required'}, 400
    
    if target_reps <= 0:
        return {'error': 'Target reps must be positive'}, 400
    
    exercises = load_exercises()
    exercise_id = str(uuid.uuid4())[:8]  # Short unique ID
    
    exercises[exercise_id] = {
        'name': name,
        'target_reps': target_reps
    }
    
    save_exercises(exercises)
    
    return jsonify({
        'id': exercise_id,
        'name': name,
        'target_reps': target_reps
    }), 201

@app.route('/api/exercises/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    """Delete an exercise"""
    exercises = load_exercises()
    
    if exercise_id not in exercises:
        return {'error': 'Exercise not found'}, 404
    
    del exercises[exercise_id]
    save_exercises(exercises)
    
    # Also delete associated workouts
    workouts = load_workouts()
    workouts = [w for w in workouts if w['exercise_id'] != exercise_id]
    save_workouts(workouts)
    
    return jsonify({'success': True})


@app.route('/exercises/<exercise_id>/delete', methods=['POST'])
def web_delete_exercise(exercise_id):
    exercises = load_exercises()
    if exercise_id not in exercises:
        flash('Exercise not found', 'danger')
        return redirect(url_for('index'))
    del exercises[exercise_id]
    save_exercises(exercises)
    # delete workouts
    workouts = load_workouts()
    workouts = [w for w in workouts if w['exercise_id'] != exercise_id]
    save_workouts(workouts)
    flash('Exercise deleted', 'success')
    return redirect(url_for('index'))

@app.route('/api/workout', methods=['POST'])
def save_workout():
    """Save a workout entry"""
    data = request.json
    
    exercise_id = data.get('exercise_id')
    weight = float(data.get('weight'))
    reps_category = data.get('reps_category')  # 'less_than_5', 'more_than_5', 'more_than_10'
    
    exercises = load_exercises()
    if not exercise_id or exercise_id not in exercises:
        return {'error': 'Invalid exercise'}, 400
    
    # Calculate next suggested weight
    next_weight = calculate_next_weight(weight, reps_category)
    
    # Create workout entry
    workout = {
        'exercise_id': exercise_id,
        'exercise_name': exercises[exercise_id]['name'],
        'weight': weight,
        'reps_category': reps_category,
        'next_weight': next_weight,
        'date': datetime.now().isoformat()
    }
    
    # Save to file
    workouts = load_workouts()
    workouts.append(workout)
    save_workouts(workouts)
    
    return jsonify(workout), 201


@app.route('/exercises/<exercise_id>')
def exercise_detail(exercise_id):
    exercises = load_exercises()
    if exercise_id not in exercises:
        flash('Exercise not found', 'danger')
        return redirect(url_for('index'))
    ex = exercises[exercise_id]
    last = get_last_workout(exercise_id)
    # If mobile, render a simplified page with server-side history
    if is_mobile_request(request):
        workouts = load_workouts()
        history = [w for w in workouts if w['exercise_id'] == exercise_id]
        history = sorted(history, key=lambda x: x['date'], reverse=True)
        return render_template('exercise_mobile.html', exercise_id=exercise_id, exercise=ex, last=last, history=history)

    return render_template('exercise.html', exercise_id=exercise_id, exercise=ex, last=last)


@app.route('/exercises/<exercise_id>/confirm-delete', methods=['GET'])
def confirm_delete_exercise(exercise_id):
    """Show confirmation page for deleting an exercise"""
    exercises = load_exercises()
    if exercise_id not in exercises:
        flash('Exercise not found', 'danger')
        return redirect(url_for('index'))
    ex = exercises[exercise_id]
    
    if is_mobile_request(request):
        return render_template('exercise_delete_confirm_mobile.html', exercise_id=exercise_id, exercise=ex)
    return render_template('exercise_delete_confirm.html', exercise_id=exercise_id, exercise=ex)

@app.route('/exercises/<exercise_id>/log', methods=['POST'])
def web_log_workout(exercise_id):
    exercises = load_exercises()
    if exercise_id not in exercises:
        flash('Invalid exercise', 'danger')
        return redirect(url_for('index'))
    try:
        weight = float(request.form.get('weight', 0))
    except ValueError:
        flash('Invalid weight', 'danger')
        return redirect(url_for('exercise_detail', exercise_id=exercise_id))
    reps_category = request.form.get('reps_category')
    next_weight = calculate_next_weight(weight, reps_category)
    workout = {
        'exercise_id': exercise_id,
        'exercise_name': exercises[exercise_id]['name'],
        'weight': weight,
        'reps_category': reps_category,
        'next_weight': next_weight,
        'date': datetime.now().isoformat()
    }
    workouts = load_workouts()
    workouts.append(workout)
    save_workouts(workouts)
    flash('Workout logged', 'success')
    return redirect(url_for('exercise_detail', exercise_id=exercise_id))


@app.route('/exercises/<exercise_id>/confirm-delete-last', methods=['GET'])
def confirm_delete_last(exercise_id):
    """Show confirmation page for deleting the most recent workout for an exercise"""
    exercises = load_exercises()
    if exercise_id not in exercises:
        flash('Exercise not found', 'danger')
        return redirect(url_for('index'))
    ex = exercises[exercise_id]
    if is_mobile_request(request):
        return render_template('exercise_delete_last_confirm_mobile.html', exercise_id=exercise_id, exercise=ex)
    return render_template('exercise_delete_last_confirm.html', exercise_id=exercise_id, exercise=ex)


@app.route('/exercises/<exercise_id>/delete-last', methods=['POST'])
def web_delete_last(exercise_id):
    """Delete the most recent workout entry for a given exercise"""
    exercises = load_exercises()
    if exercise_id not in exercises:
        flash('Invalid exercise', 'danger')
        return redirect(url_for('index'))

    workouts = load_workouts()
    # find last index with matching exercise_id
    last_index = None
    for i in range(len(workouts)-1, -1, -1):
        if workouts[i].get('exercise_id') == exercise_id:
            last_index = i
            break

    if last_index is None:
        flash('No sessions to delete for this exercise', 'warning')
        return redirect(url_for('exercise_detail', exercise_id=exercise_id))

    removed = workouts.pop(last_index)
    save_workouts(workouts)
    flash(f"Removed last session: {removed.get('weight')} kg on {removed.get('date').split('T')[0]}", 'success')
    return redirect(url_for('exercise_detail', exercise_id=exercise_id))

@app.route('/api/history')
def get_history():
    """Get all workout history"""
    workouts = load_workouts()
    return jsonify(sorted(workouts, key=lambda x: x['date'], reverse=True))

@app.route('/api/exercise-history/<exercise_id>')
def get_exercise_history(exercise_id):
    """Get workout history for a specific exercise"""
    workouts = load_workouts()
    exercise_workouts = [w for w in workouts if w['exercise_id'] == exercise_id]
    return jsonify(sorted(exercise_workouts, key=lambda x: x['date'], reverse=True))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
