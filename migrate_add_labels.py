"""
Migration script to add label column to existing database
Run this once to add the label column to existing exercises table
"""
import sqlite3
import os

def migrate_add_labels():
    db_path = os.getenv('DATABASE_PATH', 'workouts.db')
    
    # Check common locations
    possible_paths = [
        db_path,
        os.path.join('instance', db_path),
        os.path.join('instance', 'workouts.db')
    ]
    
    actual_path = None
    for path in possible_paths:
        if os.path.exists(path):
            actual_path = path
            break
    
    if not actual_path:
        print(f"Database not found in any of these locations: {possible_paths}")
        print("No migration needed - database will be created with label column on first run.")
        return
    
    print(f"Found database at: {actual_path}")
    
    conn = sqlite3.connect(actual_path)
    cursor = conn.cursor()
    
    # Check if label column already exists
    cursor.execute("PRAGMA table_info(exercises)")
    columns = [row[1] for row in cursor.fetchall()]
    
    if 'label' in columns:
        print("✓ Label column already exists. No migration needed.")
        conn.close()
        return
    
    print("Adding label column to exercises table...")
    
    try:
        # Add the label column with default value
        cursor.execute("ALTER TABLE exercises ADD COLUMN label VARCHAR(50) DEFAULT 'Additional'")
        
        # Update all existing exercises to have the default label
        cursor.execute("UPDATE exercises SET label = 'Additional' WHERE label IS NULL")
        
        conn.commit()
        print("✓ Successfully added label column and updated existing exercises")
        
        # Show count of updated exercises
        cursor.execute("SELECT COUNT(*) FROM exercises")
        count = cursor.fetchone()[0]
        print(f"✓ Updated {count} exercises with default label 'Additional'")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ Error during migration: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    migrate_add_labels()
