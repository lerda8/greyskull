"""
Automated backup script for Greyskull Workout Tracker
Run this script periodically (e.g., via cron or Task Scheduler)
to create backups of your workout database.
"""
import os
import shutil
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def backup_database():
    """Create a backup of the database"""
    db_path = os.getenv('DATABASE_PATH', os.path.join('instance', 'workouts.db'))
    backup_dir = os.getenv('BACKUP_DIR', 'backups')
    
    if not os.path.exists(db_path):
        print(f"⚠️  Database not found: {db_path}")
        return False
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"✓ Created backup directory: {backup_dir}")
    
    # Create backup with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'workouts_backup_{timestamp}.db')
    
    try:
        shutil.copy2(db_path, backup_path)
        file_size = os.path.getsize(backup_path)
        print(f"✓ Backup created: {backup_path} ({file_size} bytes)")
        
        # Keep only last 10 backups
        cleanup_old_backups(backup_dir)
        
        return True
    except Exception as e:
        print(f"✗ Backup failed: {e}")
        return False


def cleanup_old_backups(backup_dir, keep=10):
    """Keep only the most recent backups"""
    backups = sorted([
        f for f in os.listdir(backup_dir) 
        if f.startswith('workouts_backup_') and f.endswith('.db')
    ])
    
    if len(backups) > keep:
        for old_backup in backups[:-keep]:
            old_path = os.path.join(backup_dir, old_backup)
            os.remove(old_path)
            print(f"  Removed old backup: {old_backup}")


if __name__ == '__main__':
    print("=" * 50)
    print("Greyskull Workout Tracker - Backup Script")
    print("=" * 50)
    backup_database()
    print("=" * 50)
