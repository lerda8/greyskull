"""
Migration script to add is_custom_next_weight column to workouts table.
Run this once to update existing database.
"""
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

def migrate():
    db_path = os.getenv('DATABASE_PATH', 'instance/workouts.db')
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(workouts)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_custom_next_weight' in columns:
            print("✓ Column 'is_custom_next_weight' already exists. No migration needed.")
            return
        
        # Add the new column
        print("Adding 'is_custom_next_weight' column to workouts table...")
        cursor.execute("""
            ALTER TABLE workouts 
            ADD COLUMN is_custom_next_weight BOOLEAN NOT NULL DEFAULT 0
        """)
        
        conn.commit()
        print("✓ Migration completed successfully!")
        print("  - Added is_custom_next_weight column")
        print("  - All existing workouts marked as non-custom (default)")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
