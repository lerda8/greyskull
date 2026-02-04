from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response, make_response
from flask_httpauth import HTTPBasicAuth
from datetime import datetime
import json
import os
import uuid
import logging
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration from environment
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-me-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.getenv('DATABASE_PATH', 'workouts.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import and initialize database
from database import db, Exercise, Workout, init_db, backup_database

# Initialize database
init_db(app)

# Setup authentication (optional)
auth = HTTPBasicAuth()
AUTH_ENABLED = bool(os.getenv('AUTH_PASSWORD'))  # Only enable if password is set

@auth.verify_password
def verify_password(username, password):
    """Verify username and password"""
    if not AUTH_ENABLED:
        return True  # No auth required if password not set
    
    expected_username = os.getenv('AUTH_USERNAME', 'admin')
    expected_password = os.getenv('AUTH_PASSWORD', '')
    
    if username == expected_username and password == expected_password:
        return username
    return None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Jinja2 template filters
@app.template_filter('format_date')
def format_date(date_string):
    """Format date string to human-readable format"""
    try:
        # Handle both ISO format strings and datetime objects
        if isinstance(date_string, str):
            # Parse ISO format: 2024-01-15T10:30:00 or 2024-01-15
            if 'T' in date_string:
                dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            else:
                dt = datetime.strptime(date_string, '%Y-%m-%d')
        elif isinstance(date_string, datetime):
            dt = date_string
        else:
            return str(date_string)
        
        # Format as "Jan 15, 2024"
        return dt.strftime('%b %d, %Y')
    except Exception as e:
        logger.error(f"Error formatting date {date_string}: {e}")
        return str(date_string)

# Default exercises (used only for reference now)
DEFAULT_EXERCISES = {
    'ohp': {'name': 'Overhead Press / Bench Press', 'target_reps': 5},
    'rows': {'name': 'Chinups / Barbell Rows', 'target_reps': 5},
    'squats': {'name': 'Squats', 'target_reps': 5},
    'deadlifts': {'name': 'Deadlifts', 'target_reps': 1}
}

def validate_exercise_name(name):
    """Validate exercise name"""
    if not name or not isinstance(name, str):
        return False
    name = name.strip()
    if len(name) < 2 or len(name) > 200:
        return False
    return True

def validate_weight(weight):
    """Validate weight value"""
    try:
        weight = float(weight)
        if weight < 0 or weight > 1000:  # Reasonable limits
            return False
        return True
    except (ValueError, TypeError):
        return False

def validate_reps_category(category):
    """Validate reps category"""
    valid_categories = ['less_than_5', 'more_than_5', 'more_than_10']
    return category in valid_categories


def is_mobile_request(req):
    """Rudimentary mobile detection based on User-Agent header"""
    ua = (req.headers.get('User-Agent') or '').lower()
    return 'mobile' in ua or 'iphone' in ua or 'android' in ua

def get_last_workout(exercise_id):
    """Get the last workout for a specific exercise"""
    try:
        workout = Workout.query.filter_by(exercise_id=exercise_id).order_by(Workout.date.desc()).first()
        return workout.to_dict() if workout else None
    except Exception as e:
        logger.error(f"Error getting last workout: {e}")
        return None

def calculate_next_weight(current_weight, reps_category, exercise_type='upper'):
    """
    Calculate recommended next weight based on reps performed and exercise type.
    
    Rules:
    - Legs exercises: +2kg normal, +4kg for 10+ reps
    - Upper body exercises: +1kg normal, +2kg for 10+ reps
    - Less than 5 reps: -10% (deload)
    """
    # Determine base increment based on exercise type
    base_increment = 2.0 if exercise_type == 'legs' else 1.0
    
    if reps_category == 'more_than_10':
        # Hit AMRAP with 10+ reps, double the normal increase
        return round(current_weight + (base_increment * 2), 1)
    elif reps_category == 'more_than_5':
        # Hit 5+ reps, normal increase
        return round(current_weight + base_increment, 1)
    elif reps_category == 'less_than_5':
        # Didn't hit 5 reps, deload by 10%
        return round(current_weight - current_weight * 0.10, 1)
    return current_weight

@app.route('/')
@auth.login_required
def index():
    """Index: list exercises with optional label filtering"""
    try:
        # Get filter parameter
        filter_label = request.args.get('filter', None)
        
        # Query exercises
        if filter_label and filter_label != 'all':
            exercises = Exercise.query.filter_by(label=filter_label).all()
        else:
            exercises = Exercise.query.all()
        
        # Build list with last workout info
        exercises_with_history = []
        for ex in exercises:
            last = get_last_workout(ex.id)
            exercises_with_history.append({
                'id': ex.id,
                'name': ex.name,
                'label': ex.label or 'Supplemental',
                'target_reps': ex.target_reps,
                'last': last
            })
        
        # Serve a simplified mobile view when appropriate
        if is_mobile_request(request):
            return render_template('index_mobile.html', 
                                 exercises=exercises_with_history,
                                 current_filter=filter_label or 'all')
        return render_template('index.html', 
                             exercises=exercises_with_history,
                             current_filter=filter_label or 'all')
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        flash('Error loading exercises', 'danger')
        return render_template('index.html', exercises=[], current_filter='all')

@app.route('/api/exercises')
@auth.login_required
def get_exercises():
    """Get all exercises with their last workout info"""
    try:
        exercises = Exercise.query.all()
        exercises_with_history = []
        
        for exercise in exercises:
            last = get_last_workout(exercise.id)
            
            data = {
                'id': exercise.id,
                'name': exercise.name,
                'target_reps': exercise.target_reps,
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
    except Exception as e:
        logger.error(f"Error getting exercises: {e}")
        return jsonify({'error': 'Failed to load exercises'}), 500


@app.route('/exercises/add', methods=['POST'])
@auth.login_required
def web_add_exercise():
    name = request.form.get('name', '').strip()
    label = request.form.get('label', 'Supplemental').strip()
    exercise_type = request.form.get('exercise_type', 'upper').strip()
    try:
        target_reps = int(request.form.get('target_reps', 5))
    except ValueError:
        target_reps = 5

    if not validate_exercise_name(name):
        flash('Invalid exercise name', 'danger')
        return redirect(url_for('index'))

    try:
        exercise_id = str(uuid.uuid4())[:8]
        exercise = Exercise(id=exercise_id, name=name, label=label, exercise_type=exercise_type, target_reps=target_reps)
        db.session.add(exercise)
        db.session.commit()
        flash('Exercise added', 'success')
    except Exception as e:
        logger.error(f"Error adding exercise: {e}")
        db.session.rollback()
        flash('Error adding exercise', 'danger')
    
    return redirect(url_for('index'))

@app.route('/api/exercises', methods=['POST'])
@auth.login_required
def add_exercise():
    """Add a new exercise"""
    try:
        data = request.json
        name = data.get('name', '').strip()
        label = data.get('label', 'Supplemental').strip()
        exercise_type = data.get('exercise_type', 'upper').strip()
        target_reps = int(data.get('target_reps', 5))
        
        if not validate_exercise_name(name):
            return {'error': 'Invalid exercise name'}, 400
        
        if target_reps <= 0:
            return {'error': 'Target reps must be positive'}, 400
        
        if exercise_type not in ['upper', 'legs']:
            return {'error': 'Invalid exercise type'}, 400
        
        exercise_id = str(uuid.uuid4())[:8]
        exercise = Exercise(id=exercise_id, name=name, label=label, exercise_type=exercise_type, target_reps=target_reps)
        db.session.add(exercise)
        db.session.commit()
        
        return jsonify(exercise.to_dict()), 201
    except Exception as e:
        logger.error(f"Error adding exercise via API: {e}")
        db.session.rollback()
        return {'error': 'Failed to add exercise'}, 500

@app.route('/api/exercises/<exercise_id>', methods=['DELETE'])
@auth.login_required
def delete_exercise(exercise_id):
    """Delete an exercise"""
    try:
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            return {'error': 'Exercise not found'}, 404
        
        db.session.delete(exercise)
        db.session.commit()
        
        # Backup after deletion
        if os.getenv('BACKUP_ENABLED', 'True').lower() == 'true':
            backup_database(os.getenv('BACKUP_DIR', 'backups'))
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error deleting exercise: {e}")
        db.session.rollback()
        return {'error': 'Failed to delete exercise'}, 500


@app.route('/exercises/<exercise_id>/delete', methods=['POST'])
@auth.login_required
def web_delete_exercise(exercise_id):
    try:
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            flash('Exercise not found', 'danger')
            return redirect(url_for('index'))
        
        db.session.delete(exercise)
        db.session.commit()
        
        # Backup after deletion
        if os.getenv('BACKUP_ENABLED', 'True').lower() == 'true':
            backup_database(os.getenv('BACKUP_DIR', 'backups'))
        
        flash('Exercise deleted', 'success')
    except Exception as e:
        logger.error(f"Error deleting exercise: {e}")
        db.session.rollback()
        flash('Error deleting exercise', 'danger')
    
    return redirect(url_for('index'))

@app.route('/exercises/bulk-delete', methods=['POST'])
@auth.login_required
def bulk_delete_exercises():
    """Delete multiple exercises at once"""
    try:
        exercise_ids = request.form.getlist('exercise_ids')
        
        if not exercise_ids:
            flash('No exercises selected', 'warning')
            return redirect(url_for('index'))
        
        deleted_count = 0
        for exercise_id in exercise_ids:
            exercise = db.session.get(Exercise, exercise_id)
            if exercise:
                db.session.delete(exercise)
                deleted_count += 1
        
        db.session.commit()
        
        # Backup after bulk deletion
        if os.getenv('BACKUP_ENABLED', 'True').lower() == 'true':
            backup_database(os.getenv('BACKUP_DIR', 'backups'))
        
        flash(f'Successfully deleted {deleted_count} exercise(s)', 'success')
    except Exception as e:
        logger.error(f"Error in bulk delete: {e}")
        db.session.rollback()
        flash('Error deleting exercises', 'danger')
    
    return redirect(url_for('index'))

@app.route('/api/workout', methods=['POST'])
@auth.login_required
def save_workout():
    """Save a workout entry"""
    try:
        data = request.json
        
        exercise_id = data.get('exercise_id')
        weight = float(data.get('weight'))
        reps_category = data.get('reps_category')
        custom_next_weight = data.get('custom_next_weight')
        
        if not validate_weight(weight):
            return {'error': 'Invalid weight value'}, 400
        
        if not validate_reps_category(reps_category):
            return {'error': 'Invalid reps category'}, 400
        
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            return {'error': 'Invalid exercise'}, 400
        
        # Check if user provided custom next weight
        if custom_next_weight is not None:
            try:
                next_weight = float(custom_next_weight)
                if not validate_weight(next_weight):
                    return {'error': 'Invalid custom next weight'}, 400
                is_custom = True
            except (ValueError, TypeError):
                return {'error': 'Invalid custom next weight'}, 400
        else:
            # Use automatic calculation based on exercise type
            next_weight = calculate_next_weight(weight, reps_category, exercise.exercise_type or 'upper')
            is_custom = False
        
        # Create workout entry
        workout = Workout(
            exercise_id=exercise_id,
            exercise_name=exercise.name,
            weight=weight,
            reps_category=reps_category,
            next_weight=next_weight,
            is_custom_next_weight=is_custom,
            date=datetime.utcnow()
        )
        
        db.session.add(workout)
        db.session.commit()
        
        # Backup after workout
        if os.getenv('BACKUP_ENABLED', 'True').lower() == 'true':
            backup_database(os.getenv('BACKUP_DIR', 'backups'))
        
        return jsonify(workout.to_dict()), 201
    except Exception as e:
        logger.error(f"Error saving workout: {e}")
        db.session.rollback()
        return {'error': 'Failed to save workout'}, 500


@app.route('/exercises/<exercise_id>')
@auth.login_required
def exercise_detail(exercise_id):
    try:
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            flash('Exercise not found', 'danger')
            return redirect(url_for('index'))
        
        ex = exercise.to_dict()
        last = get_last_workout(exercise_id)
        
        # If mobile, render a simplified page with server-side history
        if is_mobile_request(request):
            workouts = Workout.query.filter_by(exercise_id=exercise_id).order_by(Workout.date.desc()).all()
            history = [w.to_dict() for w in workouts]
            response = make_response(render_template('exercise_mobile.html', exercise_id=exercise_id, exercise=ex, last=last, history=history))
            # Prevent caching to ensure fresh data after updates
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response

        response = make_response(render_template('exercise.html', exercise_id=exercise_id, exercise=ex, last=last))
        # Prevent caching to ensure fresh data after updates
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    except Exception as e:
        logger.error(f"Error in exercise detail: {e}", exc_info=True)
        flash('Error loading exercise', 'danger')
        return redirect(url_for('index'))


@app.route('/exercises/<exercise_id>/confirm-delete', methods=['GET'])
@auth.login_required
def confirm_delete_exercise(exercise_id):
    """Show confirmation page for deleting an exercise"""
    try:
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            flash('Exercise not found', 'danger')
            return redirect(url_for('index'))
        
        ex = exercise.to_dict()
        
        if is_mobile_request(request):
            return render_template('exercise_delete_confirm_mobile.html', exercise_id=exercise_id, exercise=ex)
        return render_template('exercise_delete_confirm.html', exercise_id=exercise_id, exercise=ex)
    except Exception as e:
        logger.error(f"Error in confirm delete: {e}")
        flash('Error loading exercise', 'danger')
        return redirect(url_for('index'))

@app.route('/exercises/<exercise_id>/log', methods=['POST'])
@auth.login_required
def web_log_workout(exercise_id):
    try:
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            flash('Invalid exercise', 'danger')
            return redirect(url_for('index'))
        
        weight = float(request.form.get('weight', 0))
        if not validate_weight(weight):
            flash('Invalid weight', 'danger')
            return redirect(url_for('exercise_detail', exercise_id=exercise_id))
        
        reps_category = request.form.get('reps_category')
        if not validate_reps_category(reps_category):
            flash('Invalid reps category', 'danger')
            return redirect(url_for('exercise_detail', exercise_id=exercise_id))
        
        # Check if user provided custom next weight
        custom_next_weight = request.form.get('custom_next_weight', '').strip()
        is_custom = False
        if custom_next_weight:
            try:
                next_weight = float(custom_next_weight)
                if not validate_weight(next_weight):
                    flash('Invalid custom next weight', 'danger')
                    return redirect(url_for('exercise_detail', exercise_id=exercise_id))
                is_custom = True
            except ValueError:
                flash('Invalid custom next weight', 'danger')
                return redirect(url_for('exercise_detail', exercise_id=exercise_id))
        else:
            # Use automatic calculation based on exercise type
            next_weight = calculate_next_weight(weight, reps_category, exercise.exercise_type or 'upper')
        
        workout = Workout(
            exercise_id=exercise_id,
            exercise_name=exercise.name,
            weight=weight,
            reps_category=reps_category,
            next_weight=next_weight,
            is_custom_next_weight=is_custom,
            date=datetime.utcnow()
        )
        
        db.session.add(workout)
        db.session.commit()
        
        # Backup after workout
        if os.getenv('BACKUP_ENABLED', 'True').lower() == 'true':
            backup_database(os.getenv('BACKUP_DIR', 'backups'))
        
        flash('Workout logged', 'success')
    except Exception as e:
        logger.error(f"Error logging workout: {e}")
        db.session.rollback()
        flash('Error logging workout', 'danger')
    
    # Add cache-busting parameter to force reload
    return redirect(url_for('exercise_detail', exercise_id=exercise_id, _t=int(time.time())))


@app.route('/exercises/<exercise_id>/confirm-delete-last', methods=['GET'])
@auth.login_required
def confirm_delete_last(exercise_id):
    """Show confirmation page for deleting the most recent workout for an exercise"""
    try:
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            flash('Exercise not found', 'danger')
            return redirect(url_for('index'))
        
        ex = exercise.to_dict()
        
        if is_mobile_request(request):
            return render_template('exercise_delete_last_confirm_mobile.html', exercise_id=exercise_id, exercise=ex)
        return render_template('exercise_delete_last_confirm.html', exercise_id=exercise_id, exercise=ex)
    except Exception as e:
        logger.error(f"Error in confirm delete last: {e}")
        flash('Error loading exercise', 'danger')
        return redirect(url_for('index'))


@app.route('/exercises/<exercise_id>/delete-last', methods=['POST'])
@auth.login_required
def web_delete_last(exercise_id):
    """Delete the most recent workout entry for a given exercise"""
    try:
        exercise = db.session.get(Exercise, exercise_id)
        if not exercise:
            flash('Invalid exercise', 'danger')
            return redirect(url_for('index'))

        # Find last workout for this exercise
        last_workout = Workout.query.filter_by(exercise_id=exercise_id).order_by(Workout.date.desc()).first()
        
        if not last_workout:
            flash('No sessions to delete for this exercise', 'warning')
            return redirect(url_for('exercise_detail', exercise_id=exercise_id))

        removed_weight = last_workout.weight
        removed_date = last_workout.date.strftime('%Y-%m-%d')
        
        db.session.delete(last_workout)
        db.session.commit()
        
        # Backup after deletion
        if os.getenv('BACKUP_ENABLED', 'True').lower() == 'true':
            backup_database(os.getenv('BACKUP_DIR', 'backups'))
        
        flash(f"Removed last session: {removed_weight} kg on {removed_date}", 'success')
    except Exception as e:
        logger.error(f"Error deleting last workout: {e}")
        db.session.rollback()
        flash('Error deleting workout', 'danger')
    
    # Add cache-busting parameter to force reload
    return redirect(url_for('exercise_detail', exercise_id=exercise_id, _t=int(time.time())))

@app.route('/api/history')
@auth.login_required
def get_history():
    """Get all workout history"""
    try:
        workouts = Workout.query.order_by(Workout.date.desc()).all()
        return jsonify([w.to_dict() for w in workouts])
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        return jsonify({'error': 'Failed to load history'}), 500

@app.route('/api/exercise-history/<exercise_id>')
@auth.login_required
def get_exercise_history(exercise_id):
    """Get workout history for a specific exercise"""
    try:
        workouts = Workout.query.filter_by(exercise_id=exercise_id).order_by(Workout.date.desc()).all()
        return jsonify([w.to_dict() for w in workouts])
    except Exception as e:
        logger.error(f"Error getting exercise history: {e}")
        return jsonify({'error': 'Failed to load history'}), 500


def _generate_svg_chart(points, width=600, height=200, padding=24):
    """Generate a simple SVG line chart from list of (datetime, weight) tuples.
    Points expected in ascending time order."""
    if not points:
        return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>
            <rect width='100%' height='100%' fill='#fff' />
            <text x='{width/2}' y='{height/2}' font-size='14' text-anchor='middle' fill='#666'>No data</text>
        </svg>"""

    # Extract x (datetime) and y (weight)
    xs = [p[0].timestamp() for p in points]
    ys = [p[1] for p in points]

    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    # If all weights equal, create a small range
    if ymin == ymax:
        ymin -= 1
        ymax += 1

    def sx(x):
        if xmax == xmin:
            return padding + (width - 2*padding)/2
        return padding + (x - xmin) / (xmax - xmin) * (width - 2*padding)

    def sy(y):
        return padding + (1 - (y - ymin) / (ymax - ymin)) * (height - 2*padding)

    # Build polyline points
    poly_pts = []
    for dt_ts, y in zip(xs, ys):
        poly_pts.append(f"{sx(dt_ts):.1f},{sy(y):.1f}")

    # Generate simple axes and labels for first and last
    first_label = points[0][0].strftime('%Y-%m-%d')
    last_label = points[-1][0].strftime('%Y-%m-%d')

    svg = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>"]
    svg.append("<rect width='100%' height='100%' fill='#ffffff'/>")
    # grid lines (horizontal)
    for i in range(5):
        yv = ymin + i * (ymax - ymin) / 4
        svg.append(f"<line x1='{padding}' y1='{sy(yv):.1f}' x2='{width-padding}' y2='{sy(yv):.1f}' stroke='#eee' stroke-width='1' />")
        svg.append(f"<text x='{padding-6}' y='{sy(yv)+4:.1f}' font-size='10' text-anchor='end' fill='#888'>{yv:.1f}</text>")

    # polyline
    svg.append(f"<polyline fill='none' stroke='#007bff' stroke-width='2' points='{' '.join(poly_pts)}' />")
    # dots
    for dt_ts, y in zip(xs, ys):
        svg.append(f"<circle cx='{sx(dt_ts):.1f}' cy='{sy(y):.1f}' r='3' fill='#007bff' />")

    # x labels
    svg.append(f"<text x='{padding}' y='{height-padding+16}' font-size='10' fill='#666'>{first_label}</text>")
    svg.append(f"<text x='{width-padding}' y='{height-padding+16}' font-size='10' text-anchor='end' fill='#666'>{last_label}</text>")

    svg.append('</svg>')
    return '\n'.join(svg)


@app.route('/exercise-chart/<exercise_id>')
@auth.login_required
def exercise_chart(exercise_id):
    """Return an SVG line chart showing weight over time for the exercise."""
    try:
        workouts = Workout.query.filter_by(exercise_id=exercise_id).order_by(Workout.date).all()
        
        if not workouts:
            svg = _generate_svg_chart([])
            return Response(svg, mimetype='image/svg+xml')

        # Convert dates and weights
        pts = []
        for workout in workouts:
            try:
                pts.append((workout.date, workout.weight))
            except Exception:
                continue

        svg = _generate_svg_chart(pts, width=700, height=220)
        return Response(svg, mimetype='image/svg+xml')
    except Exception as e:
        logger.error(f"Error generating chart: {e}")
        svg = _generate_svg_chart([])
        return Response(svg, mimetype='image/svg+xml')


# Error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    flash('Page not found', 'warning')
    return redirect(url_for('index'))


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logger.error(f"Server error: {e}", exc_info=True)
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    flash('An error occurred. Please try again.', 'danger')
    return redirect(url_for('index'))


# Debug route to check database
@app.route('/debug/db')
def debug_db():
    """Debug route to check database status"""
    try:
        exercises_count = Exercise.query.count()
        workouts_count = Workout.query.count()
        exercises = Exercise.query.all()
        
        result = {
            'exercises_count': exercises_count,
            'workouts_count': workouts_count,
            'exercises': [e.to_dict() for e in exercises]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    logger.info(f"Starting Greyskull Workout Tracker on {host}:{port} (debug={debug_mode})")
    app.run(debug=debug_mode, host=host, port=port)
