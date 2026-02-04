"""
Database migration script to add exercise_type column to exercises table.
This should be run once to update the existing database schema.
"""
import sqlite3
import os

# Path to the database
db_path = 'instance/workouts.db'

def migrate():
    """Add exercise_type column to exercises table"""
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    print(f"Connecting to database at {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(exercises)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'exercise_type' in columns:
            print("Column 'exercise_type' already exists. No migration needed.")
            conn.close()
            return
        
        print("Adding exercise_type column...")
        # Add the new column with default value 'upper'
        cursor.execute("""
            ALTER TABLE exercises 
            ADD COLUMN exercise_type VARCHAR(20) NOT NULL DEFAULT 'upper'
        """)
        
        # Update specific exercises that are leg exercises
        print("Setting exercise_type for known leg exercises...")
        cursor.execute("""
            UPDATE exercises 
            SET exercise_type = 'legs' 
            WHERE LOWER(name) LIKE '%squat%' 
               OR LOWER(name) LIKE '%deadlift%'
               OR LOWER(name) LIKE '%leg press%'
               OR LOWER(name) LIKE '%lunge%'
        """)
        
        rows_updated = cursor.rowcount
        print(f"Updated {rows_updated} exercises to 'legs' type")
        
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
