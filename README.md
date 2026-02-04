# Greyskull LP Workout Tracker

A sleek, mobile-first fitness tracking web application designed for the Greyskull LP (Linear Progression) strength training program. Built for iPhone 12 Mini and optimized for seamless workout logging at the gym.

## ✨ Features

### Core Functionality
- 📊 **Exercise Management**: Add, organize, and delete exercises with workout labels (Workout A, Workout B, Supplemental)
- 💪 **Smart Workout Logging**: Record weight and reps with auto-calculated progressive overload
- 📈 **Progress Tracking**: View workout history with human-readable dates and session counts
- 🎯 **Custom Next Weight**: Override automatic progression when needed with custom weight targets
- 🏋️ **Plate Calculator**: Real-time calculation showing exactly which gym plates to load per side (20kg bar)
- 📱 **Mobile-First Design**: Beautifully optimized for iPhone 12 Mini (375px) with smooth animations
- 🔄 **Exercise Type Support**: Different weight increments for upper body (+1kg/+2kg) vs legs (+2kg/+4kg)
- ✨ **Smooth Animations**: Cascading fade-in effects when switching between workout labels and viewing exercises

### User Experience
- 🎨 **Modern UI**: Clean gradient designs, custom cards, and professional typography
- 🗑️ **Bulk Operations**: Select and delete multiple exercises at once with custom confirmation modals
- 🔒 **Optional Authentication**: HTTP Basic Auth for secure access
- 💾 **Automatic Backups**: Database backed up after every workout
- 🌐 **Cloudflare Tunnel Ready**: Perfect for secure remote gym access

### Progressive Overload Logic
- **< 5 reps**: Deload by 10%
- **5-9 reps**: Maintain current weight (increment by base amount)
- **10+ reps**: Double increment
  - Upper body exercises: +1kg normally, +2kg for 10+ reps
  - Leg exercises (squats, deadlifts): +2kg normally, +4kg for 10+ reps

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

Run the migration scripts to set up the database with all features:

```bash
# Add exercise type support (upper body vs legs)
python migrate_add_exercise_type.py

# Add custom next weight flag
python migrate_add_labels.py
```

### 3. Run the Application

```bash
python app.py
```

Or use the PowerShell start script:
```powershell
.\start.ps1
```

The app will:
- ✅ Create the SQLite database at `instance/workouts.db`
- ✅ Start the Flask development server
- ✅ Open at `http://localhost:5000`

### 4. Access the App

Open your browser and go to:
- Local: `http://localhost:5000`
- Network: `http://<your-ip>:5000`

If you set `AUTH_PASSWORD`, you'll need to login with:
- Username: `admin` (or whatever you set in `AUTH_USERNAME`)
- Password: your configured password

## Configuration

All configuration is done via the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key (CHANGE THIS!) | `greyskull-workout-secret-change-me-in-production` |
| `FLASK_DEBUG` | Enable debug mode | `True` |
| `FLASK_HOST` | Server host | `0.0.0.0` |
| `FLASK_PORT` | Server port | `5000` |
| `DATABASE_PATH` | SQLite database file | `workouts.db` |
| `AUTH_USERNAME` | Login username | `admin` |
| `AUTH_PASSWORD` | Login password (leave empty to disable auth) | _(empty)_ |
| `BACKUP_DIR` | Backup directory | `backups` |
| `BACKUP_ENABLED` | Enable automatic backups | `True` |

## Remote Access with Cloudflare Tunnel

Perfect for accessing your tracker remotely without exposing ports:

1. Install cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/
2. Start your app: `python app.py`
3. Create tunnel: `cloudflared tunnel --url http://localhost:5000`
4. Access via the provided URL

**Pro tip**: Set up a permanent tunnel for persistent access!

## Backups

### Automatic Backups
The app automatically backs up your database:
- After every workout logged
- After exercise deletions
- Keeps last 10 backups in `backups/` directory

### Manual Backup
Run the backup script anytime:
```bash
python backup.py
```

### Restore from Backup
1. Stop the app
2. Copy backup file: `cp backups/workouts_backup_TIMESTAMP.db workouts.db`
3. Restart the app

## Data Migration

If you have existing JSON files (`exercises.json`, `workouts.json`), they will be automatically migrated to SQLite on first run. Your JSON files are preserved as backup.

## Project Structure

```
greyskull-main/
├── app.py                 # Main Flask application
├── database.py            # Database models and migration
├── backup.py             # Backup utility script
├── requirements.txt      # Python dependencies
├── .env                  # Configuration (create from .env.example)
├── .env.example          # Configuration template
├── .gitignore           # Git ignore rules
├── workouts.db          # SQLite database (created automatically)
├── backups/             # Backup directory (created automatically)
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── exercise.html
│   └── ...
└── static/
    └── css/
        └── style.css
```

## Security Notes

For personal use on your home server:

1. **Change the SECRET_KEY**: Generate a random key
2. **Set AUTH_PASSWORD**: Even for personal use, protect your data
3. **Use HTTPS**: Cloudflare Tunnel provides this automatically
4. **Regular Backups**: The app does this automatically, but verify!

## Troubleshooting

### Database locked error
- Only one instance of the app should run at a time
- Make sure no other process is accessing `workouts.db`

### Authentication not working
- Check `AUTH_PASSWORD` is set in `.env`
- Username is case-sensitive (default: `admin`)

### Can't access remotely
- Check firewall settings
- Use Cloudflare Tunnel for secure access without port forwarding

## Development

Running in development mode:
```bash
# .env file
FLASK_DEBUG=True

python app.py
```

## License

Personal project - use freely for your own fitness tracking!

## Contributing

This is a personal project, but suggestions and improvements are welcome!

---

**Track your gains, achieve your goals! 💪**
