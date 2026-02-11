# 🏋️ Greyskull LP Tracker# Greyskull LP Workout Tracker



A clean, self-hosted workout tracker purpose-built for the [Greyskull LP](https://strengthvillain.myshopify.com/collections/all) strength training program. Track your lifts, log your AMRAP sets, and let the app handle progression math automatically.A sleek, mobile-first fitness tracking web application designed for the Greyskull LP (Linear Progression) strength training program. Built for iPhone 12 Mini and optimized for seamless workout logging at the gym.



![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)## ✨ Features

![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)

![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)### Core Functionality

![License](https://img.shields.io/badge/License-MIT-green)- 📊 **Exercise Management**: Add, organize, and delete exercises with workout labels (Workout A, Workout B, Supplemental)

- 💪 **Smart Workout Logging**: Record weight and reps with auto-calculated progressive overload

---- 📈 **Progress Tracking**: View workout history with human-readable dates and session counts

- 🎯 **Custom Next Weight**: Override automatic progression when needed with custom weight targets

## ✨ Features- 🏋️ **Plate Calculator**: Real-time calculation showing exactly which gym plates to load per side (20kg bar)

- 📱 **Mobile-First Design**: Beautifully optimized for iPhone 12 Mini (375px) with smooth animations

### Automatic Greyskull LP Progression- 🔄 **Exercise Type Support**: Different weight increments for upper body (+1kg/+2kg) vs legs (+2kg/+4kg)

- ✨ **Smooth Animations**: Cascading fade-in effects when switching between workout labels and viewing exercises

The app calculates your next working weight based on standard Greyskull LP rules:

### User Experience

| Performance | Upper Body | Legs |- 🎨 **Modern UI**: Clean gradient designs, custom cards, and professional typography

|---|---|---|- 🗑️ **Bulk Operations**: Select and delete multiple exercises at once with custom confirmation modals

| **10+ reps** on AMRAP set | +2 kg | +4 kg |- 🔒 **Optional Authentication**: HTTP Basic Auth for secure access

| **5–9 reps** on AMRAP set | +1 kg | +2 kg |- 💾 **Automatic Backups**: Database backed up after every workout

| **Under 5 reps** (failed) | −10% deload | −10% deload |- 🌐 **Cloudflare Tunnel Ready**: Perfect for secure remote gym access



You can always override the suggested weight with a custom value.### Progressive Overload Logic

- **< 5 reps**: Deload by 10%

### Everything You Need- **5-9 reps**: Maintain current weight (increment by base amount)

- **10+ reps**: Double increment

- **📊 Progress Charts** — Sparkline graphs showing weight progression over time  - Upper body exercises: +1kg normally, +2kg for 10+ reps

- **🔢 Plate Calculator** — Shows exactly which plates to load on each side of the bar (20 kg barbell)  - Leg exercises (squats, deadlifts): +2kg normally, +4kg for 10+ reps

- **📅 Date Backfill** — Log workouts from past dates you forgot to track

- **📝 Session Notes** — Attach optional notes to any workout entry## 🚀 Quick Start

- **🏷️ Exercise Labels** — Organize into Workout A, Workout B, or Supplemental

- **🔍 Filter by Label** — Quick-filter pills on the main dashboard### Prerequisites

- **📦 Bulk Operations** — Select multiple exercises for batch deletion- Python 3.8 or higher

- **⚡ Expandable History** — Shows last 5 entries with a toggle to reveal all- pip package manager

- **🗑️ Undo Last Session** — Remove the most recent log entry with a confirmation step

### 1. Install Dependencies

### Polished UI/UX

```bash

- **📱 Mobile-First Design** — Separate optimized templates for mobile and desktoppip install -r requirements.txt

- **🎨 Warm Color Palette** — Teal, orange, and sage green — easy on the eyes```

- **🔔 Toast Notifications** — Auto-dismissing success/error messages

- **🛡️ Double-Submit Protection** — Prevents accidental duplicate logs### 2. Initialize Database

- **⏳ Loading States** — Visual feedback during form submissions

- **✨ Smooth Animations** — Cascading fade-ins and transitions throughoutRun the migration scripts to set up the database with all features:



### Data Safety```bash

# Add exercise type support (upper body vs legs)

- **💾 Automatic Backups** — Database backed up after every write operationpython migrate_add_exercise_type.py

- **🔄 Backup Rotation** — Keeps last 10 backups, cleans up older ones automatically

- **🔒 Optional Auth** — HTTP Basic Auth via environment variable (disabled by default)# Add custom next weight flag

- **✅ Input Validation** — Server-side validation on all inputspython migrate_add_labels.py

```

---

### 3. Run the Application

## 🚀 Quick Start

```bash

### Prerequisitespython app.py

```

- Python 3.8 or higher

Or use the PowerShell start script:

### Setup```powershell

.\start.ps1

```bash```

# Clone the repository

git clone https://github.com/yourusername/greyskull.gitThe app will:

cd greyskull- ✅ Create the SQLite database at `instance/workouts.db`

- ✅ Start the Flask development server

# Install dependencies- ✅ Open at `http://localhost:5000`

pip install -r requirements.txt

### 4. Access the App

# Copy environment config

cp .env.example .envOpen your browser and navigate to:

- **Local**: `http://localhost:5000`

# Start the app- **Network**: `http://<your-ip>:5000`

python app.py

```The app automatically detects mobile browsers and serves an optimized mobile interface.



**Windows users** can run the one-click setup script instead:## 📲 Usage Guide



```powershell### Adding an Exercise

.\start.ps11. Tap the **+** floating action button

```2. Enter exercise name and target reps (e.g., "5x5" or "3x5+")

3. Select workout label (Workout A, Workout B, or Supplemental)

The app will be available at **http://localhost:5000**4. Choose exercise type:

   - **Upper Body**: Bench press, overhead press, rows, etc. (+1kg/+2kg increments)

### Migrating from JSON   - **Legs**: Squats, deadlifts (+2kg/+4kg increments)



If you have existing `exercises.json` and `workouts.json` files from a previous version, just place them in the project root. The app will automatically migrate them to SQLite on first startup — your JSON files are preserved as backup.### Logging a Workout

1. Tap an exercise card from the main screen

---2. Enter the weight lifted (pre-filled with your next goal)

3. Select reps achieved on final AMRAP set:

## ⚙️ Configuration   - **< 5 reps**: Weight will decrease by 10%

   - **5+ reps**: Weight increases by base increment

All configuration is done through a `.env` file. Copy `.env.example` to get started:   - **10+ reps**: Weight increases by double increment

4. (Optional) Tap **Customize** to set a custom next weight instead of auto-calculated

```env5. Review the plate calculator to see which plates to load

# Flask6. Tap **Log Workout**

SECRET_KEY=change-me-to-something-random

FLASK_DEBUG=False### Plate Calculator

FLASK_HOST=0.0.0.0The app shows exactly which Olympic plates to add per side of the bar:

FLASK_PORT=5000- 🔴 25kg (red), 🟡 20kg (yellow), 🔵 15kg (blue), 🟢 10kg (green)

- ⚫ 5kg (grey), 🔴 2.5kg (small red), ⚫ 1.25kg (black)

# Authentication (leave AUTH_PASSWORD empty to disable)- Calculates for standard 20kg Olympic barbell

AUTH_USERNAME=admin- Shows warning if weight can't be made with available plates

AUTH_PASSWORD=

### Filtering Exercises

# DatabaseUse the filter pills at the top to view:

DATABASE_PATH=workouts.db- **All**: Every exercise

- **Workout A**: Main compound lifts for Day A

# Backups- **Workout B**: Main compound lifts for Day B

BACKUP_DIR=backups- **Supplemental**: Accessory and assistance work

BACKUP_ENABLED=True

```### Bulk Delete

1. Tap **Select** in the top right

| Variable | Default | Description |2. Check exercises to delete

|---|---|---|3. Tap **Delete X Exercise(s)**

| `SECRET_KEY` | `change-me-in-production` | Flask session secret — **change this** |4. Confirm deletion (⚠️ this also deletes all workout history)

| `FLASK_DEBUG` | `False` | Enable debug mode (never in production) |

| `FLASK_HOST` | `0.0.0.0` | Bind address |### Custom Next Weight

| `FLASK_PORT` | `5000` | Port number |When logging a workout, you can override the automatic progression:

| `AUTH_USERNAME` | `admin` | Login username |1. Tap **Customize** in the "Next Session Weight" section

| `AUTH_PASSWORD` | *(empty)* | Set a password to enable auth; leave blank to disable |2. Enter your desired weight

| `DATABASE_PATH` | `workouts.db` | SQLite database file path |3. The workout will be marked with a purple **"Custom"** badge in history

| `BACKUP_DIR` | `backups` | Where automatic backups are stored |4. Tap **Use Auto** to return to automatic calculation

| `BACKUP_ENABLED` | `True` | Toggle automatic backups |

## ⚙️ Configuration

---

The app uses Flask's built-in configuration. Key settings in `app.py`:

## 🔌 REST API

```python

All endpoints require authentication when `AUTH_PASSWORD` is set.app.config['SECRET_KEY'] = 'your-secret-key-here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workouts.db'

### Exercises```



| Method | Endpoint | Description |### Optional HTTP Basic Auth

|---|---|---|To enable password protection, uncomment the authentication decorator in `app.py`:

| `GET` | `/api/exercises` | List all exercises with last workout info |

| `POST` | `/api/exercises` | Create a new exercise |```python

| `DELETE` | `/api/exercises/<id>` | Delete an exercise and all its history |@auth.login_required  # Uncomment this line

def index():

### Workouts    # ...

```

| Method | Endpoint | Description |

|---|---|---|Then set credentials:

| `POST` | `/api/workout` | Log a workout session |```python

| `GET` | `/api/history` | Get all workout history |@auth.verify_password

| `GET` | `/api/exercise-history/<id>` | Get history for a specific exercise |def verify_password(username, password):

    if username == 'admin' and password == 'your-password-here':

### Charts        return username

```

| Method | Endpoint | Description |

|---|---|---|## 📁 Project Structure

| `GET` | `/exercise-chart/<id>` | SVG line chart of weight over time |

```

<details>greyskull-main/

<summary><strong>Example: Log a workout</strong></summary>├── app.py                              # Main Flask application (746 lines)

├── database.py                         # SQLAlchemy models

```bash├── backup.py                          # Backup utility script

curl -X POST http://localhost:5000/api/workout \├── migrate_add_exercise_type.py       # Migration: exercise types

  -H "Content-Type: application/json" \├── migrate_add_labels.py              # Migration: workout labels

  -u admin:yourpassword \├── requirements.txt                   # Python dependencies

  -d '{├── start.ps1                          # PowerShell start script

    "exercise_id": "abc12345",├── README.md                          # This file

    "weight": 60,├── SETUP.md                           # Detailed setup guide

    "reps_category": "more_than_10"├── UPGRADE_SUMMARY.md                 # Version history

  }'├── LABELS_FEATURE.md                  # Labels feature docs

```├── MOBILE_UX_IMPROVEMENTS.md          # Mobile UX changelog

├── instance/

**`reps_category` values:** `less_than_5` · `more_than_5` · `more_than_10`│   └── workouts.db                    # SQLite database

├── backups/                           # Automatic backups

Optional field: `"custom_next_weight": 65` to override automatic progression.│   └── workouts_backup_*.db

├── templates/                         # Jinja2 templates

</details>│   ├── base.html                      # Base template

│   ├── base_new.html                  # Alternative base

<details>│   ├── index.html                     # Desktop exercise list

<summary><strong>Example: Add an exercise</strong></summary>│   ├── index_mobile.html              # Mobile exercise list ⭐

│   ├── exercise.html                  # Desktop exercise detail

```bash│   ├── exercise_mobile.html           # Mobile exercise detail ⭐

curl -X POST http://localhost:5000/api/exercises \│   ├── exercise_delete_confirm.html

  -H "Content-Type: application/json" \│   ├── exercise_delete_confirm_mobile.html

  -u admin:yourpassword \│   ├── exercise_delete_last_confirm.html

  -d '{│   └── exercise_delete_last_confirm_mobile.html

    "name": "Bench Press",└── static/

    "label": "Workout A",    └── css/

    "exercise_type": "upper",        └── style.css                  # Global styles

    "target_reps": 5```

  }'

```## 🗄️ Database Schema



**`exercise_type`:** `upper` (±1/2 kg increments) or `legs` (±2/4 kg increments)### Exercises Table

| Column | Type | Description |

**`label`:** `Workout A` · `Workout B` · `Supplemental`|--------|------|-------------|

| `id` | Integer | Primary key |

</details>| `name` | String | Exercise name |

| `target_reps` | String | Rep scheme (e.g., "3x5+") |

---| `label` | String | Workout A/B/Supplemental |

| `exercise_type` | String | "upper" or "legs" |

## 📁 Project Structure

### Workouts Table

```| Column | Type | Description |

greyskull/|--------|------|-------------|

├── app.py                  # Flask app — routes, progression logic, chart generation| `id` | Integer | Primary key |

├── database.py             # SQLAlchemy models, JSON → SQLite migration| `exercise_id` | Integer | Foreign key to exercises |

├── backup.py               # Standalone backup script (cron / Task Scheduler)| `weight` | Float | Weight lifted (kg) |

├── requirements.txt        # Python dependencies| `reps_category` | String | less_than_5/more_than_5/more_than_10 |

├── .env.example            # Environment configuration template| `next_weight` | Float | Calculated next session weight |

├── .gitignore| `is_custom_next_weight` | Boolean | True if user overrode auto-calculation |

├── start.ps1               # Windows one-click setup & launch| `date` | String | ISO format date |

│| `notes` | Text | Optional workout notes |

├── templates/

│   ├── base.html                              # Shared layout, CSS variables, toast system## Remote Access with Cloudflare Tunnel

│   ├── index.html                             # Desktop — exercise dashboard

│   ├── index_mobile.html                      # Mobile  — exercise dashboardPerfect for accessing your tracker remotely without exposing ports:

│   ├── exercise.html                          # Desktop — exercise detail & log form

│   ├── exercise_mobile.html                   # Mobile  — exercise detail & log form1. Install cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/

│   ├── exercise_edit.html                     # Desktop — edit exercise properties2. Start your app: `python app.py`

│   ├── exercise_edit_mobile.html              # Mobile  — edit exercise properties3. Create tunnel: `cloudflared tunnel --url http://localhost:5000`

│   ├── exercise_delete_confirm.html           # Desktop — delete exercise confirmation4. Access via the provided URL

│   ├── exercise_delete_confirm_mobile.html    # Mobile  — delete exercise confirmation

│   ├── exercise_delete_last_confirm.html      # Desktop — undo last session confirmation**Pro tip**: Set up a permanent tunnel for persistent access!

│   └── exercise_delete_last_confirm_mobile.html  # Mobile — undo last session confirmation

│## 💾 Backups

├── static/css/style.css    # Additional stylesheet

├── instance/workouts.db    # SQLite database (auto-created)### Automatic Backups

└── backups/                # Auto-rotating database backupsThe app automatically backs up your database to the `backups/` directory:

```- After every workout logged

- After exercise deletions

---- Timestamped filenames: `workouts_backup_YYYYMMDD_HHMMSS.db`



## 🛠️ Tech Stack### Manual Backup

Run the backup script anytime:

| Layer | Technology |```bash

|---|---|python backup.py

| **Backend** | [Flask 3.0](https://flask.palletsprojects.com/) + [Flask-SQLAlchemy 3.1](https://flask-sqlalchemy.palletsprojects.com/) |```

| **Database** | SQLite — zero config, single file, fully portable |

| **Auth** | [Flask-HTTPAuth 4.8](https://flask-httpauth.readthedocs.io/) (HTTP Basic) |### Restore from Backup

| **Frontend** | [Bootstrap 5.3](https://getbootstrap.com/) CDN + vanilla JavaScript |1. Stop the Flask application

| **Config** | [python-dotenv](https://github.com/theskumar/python-dotenv) |2. Replace current database:

   ```bash

---   cp backups/workouts_backup_20260204_143022.db instance/workouts.db

   ```

## 💾 Backups3. Restart the application



The app automatically backs up the SQLite database after every workout log, edit, or deletion. Backups are stored in the `backups/` directory with timestamps:## 🔧 Troubleshooting



```### Port already in use

backups/If port 5000 is occupied:

├── workouts_backup_20260115_103045.db```bash

├── workouts_backup_20260115_141522.db# Find the process

└── workouts_backup_20260116_090012.dbnetstat -ano | findstr :5000

```

# Kill it (Windows)

Only the **10 most recent** backups are kept — older ones are cleaned up automatically.taskkill /PID <process_id> /F



You can also run the standalone backup script manually or on a schedule:# Or change the port in app.py

app.run(host='0.0.0.0', port=5001, debug=True)

```bash```

python backup.py

```### Database locked error

- Only one instance should run at a time

**To restore from a backup:** copy a backup file over `instance/workouts.db` and restart the app.- Ensure no other process is accessing `instance/workouts.db`

- Check that backups aren't running simultaneously

---

### Migrations not applying

## 🤝 ContributingIf you encounter issues with migrations:

```bash

1. Fork the repository# Check database structure

2. Create a feature branch (`git checkout -b feature/my-feature`)sqlite3 instance/workouts.db ".schema"

3. Commit your changes (`git commit -am 'Add my feature'`)

4. Push to the branch (`git push origin feature/my-feature`)# Manually run migrations in order

5. Open a Pull Requestpython migrate_add_exercise_type.py

python migrate_add_labels.py

---```



## 📄 License### Mobile interface not showing

The app detects mobile browsers via User-Agent string. If not working:

This project is licensed under the [MIT License](LICENSE).- Clear browser cache

- Check `request.user_agent.platform` in Flask
- Force mobile view by accessing `index_mobile` route directly

## 🎨 Design Features

### Color Scheme
- **Neutral backgrounds**: `#ffffffad` (semi-transparent white) for cards and buttons
- **Primary gradient**: Purple/blue (`#667eea` to `#764ba2`) for branding
- **Success gradient**: Green (`#00b894` to `#00a885`) for next weight goals
- **Warning**: Orange (`#f39c12`) for ready-to-start states
- **Danger**: Red (`#e74c3c`) for delete actions

### Animations
- **Filter transitions**: Cascading fade-in with staggered delays (0.05s intervals)
- **Exercise cards**: Fade-in from 20px below with smooth ease-out
- **Touch feedback**: Active states with scale transforms

### Typography
- **Headings**: System font stack with tight letter-spacing (-0.8px)
- **Buttons**: 1.2rem, font-weight 700 for consistency
- **Dates**: Human-readable format (e.g., "Feb 04, 2026")

### Mobile Optimizations
- 44px minimum tap targets for iOS guidelines
- Safe area insets for iPhone notch/home indicator
- Gradient backdrops with backdrop-filter blur
- Touch-friendly radio buttons for rep selection
- Floating action button (FAB) for adding exercises

## 🌐 Remote Access with Cloudflare Tunnel

Perfect for accessing your tracker at the gym without exposing ports or configuring your router:

### Quick Setup
1. Install cloudflared: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/
2. Start your app: `python app.py`
3. Create tunnel in a new terminal:
   ```bash
   cloudflared tunnel --url http://localhost:5000
   ```
4. Access via the provided temporary URL (e.g., `https://random-words.trycloudflare.com`)

### Permanent Tunnel
For a persistent URL that doesn't change:
```bash
# Login to Cloudflare
cloudflared tunnel login

# Create a named tunnel
cloudflared tunnel create greyskull-tracker

# Configure tunnel (edit ~/.cloudflared/config.yml)
tunnel: <Tunnel-UUID>
credentials-file: /path/to/<Tunnel-UUID>.json

ingress:
  - hostname: greyskull.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404

# Route DNS
cloudflared tunnel route dns greyskull-tracker greyskull.yourdomain.com

# Run tunnel
cloudflared tunnel run greyskull-tracker
```

## 🔐 Security Notes

For personal use:

1. **Secret Key**: Change the `SECRET_KEY` in `app.py` to a random value
2. **HTTPS**: Cloudflare Tunnel automatically provides HTTPS encryption
3. **Authentication**: Enable HTTP Basic Auth if exposing to the internet
4. **Backups**: Verify automatic backups are working (check `backups/` directory)
5. **Local Network**: If only using at home, no authentication needed

## 🛠️ Development

### Running in Debug Mode
Debug mode is enabled by default in `app.py`:
```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Testing Mobile UI
1. Access from your phone on the same network: `http://<computer-ip>:5000`
2. Use browser dev tools mobile emulation (iPhone 12 Mini preset)
3. The app automatically serves mobile templates based on User-Agent

### Adding New Features
Key files to modify:
- `app.py`: Add routes and backend logic
- `database.py`: Modify database models
- `templates/exercise_mobile.html`: Mobile exercise detail page
- `templates/index_mobile.html`: Mobile exercise list page
- `static/css/style.css`: Global styles

### Creating Migrations
When adding database columns:
```python
# Create migration file: migrate_add_feature.py
import sqlite3

conn = sqlite3.connect('instance/workouts.db')
cursor = conn.cursor()

# Add your column
cursor.execute('ALTER TABLE exercises ADD COLUMN new_field TEXT')

conn.commit()
conn.close()
```

## 📊 Tech Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Vanilla JavaScript, Jinja2 templates
- **Styling**: Custom CSS with CSS variables and gradients
- **Mobile Detection**: User-Agent parsing
- **Date Formatting**: Python datetime + Jinja2 filters

## 📝 Dependencies

```
Flask==3.0.0
Flask-SQLAlchemy==3.0.5
Werkzeug==3.0.0
```

Install with: `pip install -r requirements.txt`

## 🤝 Contributing

This is a personal project optimized for iPhone 12 Mini, but improvements are welcome!

### Areas for Enhancement
- [ ] Export workout data to CSV
- [ ] Import exercises from templates
- [ ] Dark mode support
- [ ] Progressive Web App (PWA) capabilities
- [ ] Workout streak tracking
- [ ] Exercise notes/form cues
- [ ] 1RM calculator
- [ ] Volume tracking (sets × reps × weight)

## 📄 License

Personal fitness tracking project. Feel free to fork and adapt for your own use!

---

**Built with 💪 for serious lifters who track their progress**

*Designed for Greyskull LP, optimized for iPhone 12 Mini, perfect for the gym floor.*
