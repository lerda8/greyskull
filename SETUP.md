# Quick Setup Guide for Greyskull Workout Tracker

## First Time Setup (5 minutes)

### Step 1: Install Python packages
```powershell
pip install -r requirements.txt
```

### Step 2: Configure your settings
1. Open `.env` file in a text editor
2. Change these important settings:
   ```
   SECRET_KEY=change-this-to-something-random
   AUTH_PASSWORD=your-password-here
   FLASK_DEBUG=False
   ```

### Step 3: Run the app
```powershell
python app.py
```

### Step 4: Access the app
Open browser: http://localhost:5000
You will be redirected to `/login`; enter the credentials:
- Username: admin (or whatever you set in `AUTH_USERNAME`)
- Password: (whatever you set in `AUTH_PASSWORD`)

## That's it! 🎉

Your existing workout data from JSON files will be automatically migrated to SQLite.

## What happens on first run?
✓ Creates SQLite database (workouts.db)
✓ Migrates data from exercises.json and workouts.json
✓ Creates backups/ directory
✓ Starts the web server

## Common Commands

### Run the app
```powershell
python app.py
```

### Create manual backup
```powershell
python backup.py
```

### Check if everything is working
1. Open http://localhost:5000
2. Login (if password is set)
3. You should see your exercises

## Need Remote Access?

### Using Cloudflare Tunnel (Recommended)
1. Install cloudflared from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
2. Run: `python app.py` (in one terminal)
3. Run: `cloudflared tunnel --url http://localhost:5000` (in another terminal)
4. Access via the URL cloudflared provides

## Troubleshooting

### "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

### "Access Denied" or authentication issues
- Check AUTH_PASSWORD is set in .env file
- Default username is "admin"

### Can't access from phone/other device
- Make sure both devices are on same network
- Use your computer's IP instead of localhost
- Example: http://192.168.1.100:5000

### Port already in use
Change the port in .env:
```
FLASK_PORT=5001
```

## Security Checklist

Before using remotely:
- [ ] Changed SECRET_KEY in .env
- [ ] Set strong AUTH_PASSWORD in .env
- [ ] Set FLASK_DEBUG=False in .env
- [ ] Backups are enabled (BACKUP_ENABLED=True)

## File Locations

- Configuration: `.env`
- Database: `workouts.db`
- Backups: `backups/` folder
- Old data: `exercises.json`, `workouts.json` (kept as backup)

---

**Questions?** Check README.md for detailed documentation.
