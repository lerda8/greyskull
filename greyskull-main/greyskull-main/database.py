"""
Database models and utilities for the Greyskull workout tracker.
Includes automatic migration from JSON to SQLite.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os

db = SQLAlchemy()

class Exercise(db.Model):
    """Exercise model"""
    __tablename__ = 'exercises'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    label = db.Column(db.String(50), nullable=True, default='Supplemental')  # Workout A, Workout B, Supplemental
    exercise_type = db.Column(db.String(20), nullable=False, default='upper')  # 'legs' or 'upper'
    target_reps = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to workouts
    workouts = db.relationship('Workout', backref='exercise', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'label': self.label or 'Supplemental',
            'exercise_type': self.exercise_type or 'upper',
            'target_reps': self.target_reps
        }


class Workout(db.Model):
    """Workout session model"""
    __tablename__ = 'workouts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_id = db.Column(db.String(50), db.ForeignKey('exercises.id'), nullable=False)
    exercise_name = db.Column(db.String(200), nullable=False)  # Denormalized for history
    weight = db.Column(db.Float, nullable=False)
    reps_category = db.Column(db.String(20), nullable=False)  # less_than_5, more_than_5, more_than_10
    next_weight = db.Column(db.Float, nullable=False)
    is_custom_next_weight = db.Column(db.Boolean, default=False, nullable=False)  # Track if next weight was custom
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'exercise_id': self.exercise_id,
            'exercise_name': self.exercise_name,
            'weight': self.weight,
            'reps_category': self.reps_category,
            'next_weight': self.next_weight,
            'is_custom_next_weight': self.is_custom_next_weight,
            'date': self.date.isoformat(),
            'notes': self.notes
        }


def init_db(app):
    """Initialize database and perform migration from JSON if needed"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if we need to migrate from JSON
        migrate_from_json_if_needed()


def migrate_from_json_if_needed():
    """Migrate data from JSON files to SQLite if database is empty"""
    
    # Check if database already has data
    if Exercise.query.first() is not None:
        print("Database already initialized, skipping migration.")
        return
    
    exercises_file = 'exercises.json'
    workouts_file = 'workouts.json'
    
    migrated_exercises = 0
    migrated_workouts = 0
    
    # Migrate exercises
    if os.path.exists(exercises_file):
        try:
            with open(exercises_file, 'r') as f:
                exercises_data = json.load(f)
            
            for ex_id, ex_data in exercises_data.items():
                exercise = Exercise(
                    id=ex_id,
                    name=ex_data.get('name', 'Unknown'),
                    label=ex_data.get('label', 'Supplemental'),  # Default to Supplemental if not specified
                    target_reps=ex_data.get('target_reps', 5)
                )
                db.session.add(exercise)
                migrated_exercises += 1
            
            db.session.commit()
            print(f"✓ Migrated {migrated_exercises} exercises from JSON to SQLite")
        except Exception as e:
            print(f"Error migrating exercises: {e}")
            db.session.rollback()
    
    # Migrate workouts
    if os.path.exists(workouts_file):
        try:
            with open(workouts_file, 'r') as f:
                workouts_data = json.load(f)
            
            for workout_data in workouts_data:
                # Parse date
                date_str = workout_data.get('date')
                try:
                    workout_date = datetime.fromisoformat(date_str)
                except:
                    workout_date = datetime.utcnow()
                
                workout = Workout(
                    exercise_id=workout_data.get('exercise_id'),
                    exercise_name=workout_data.get('exercise_name', 'Unknown'),
                    weight=float(workout_data.get('weight', 0)),
                    reps_category=workout_data.get('reps_category', 'more_than_5'),
                    next_weight=float(workout_data.get('next_weight', 0)),
                    date=workout_date,
                    notes=workout_data.get('notes')
                )
                db.session.add(workout)
                migrated_workouts += 1
            
            db.session.commit()
            print(f"✓ Migrated {migrated_workouts} workouts from JSON to SQLite")
        except Exception as e:
            print(f"Error migrating workouts: {e}")
            db.session.rollback()
    
    if migrated_exercises > 0 or migrated_workouts > 0:
        print(f"\n✓ Migration complete: {migrated_exercises} exercises, {migrated_workouts} workouts")
        print("Your JSON files are preserved as backup. Database is now being used.")


def backup_database(backup_dir='backups'):
    """Create a backup of the database"""
    import shutil
    from datetime import datetime
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    db_path = db.engine.url.database
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'workouts_backup_{timestamp}.db')
        shutil.copy2(db_path, backup_path)
        
        # Keep only last 10 backups
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('workouts_backup_')])
        if len(backups) > 10:
            for old_backup in backups[:-10]:
                os.remove(os.path.join(backup_dir, old_backup))
        
        return backup_path
    return None
