# 🏋️ Greyskull LP Tracker

A clean, self-hosted workout tracker purpose-built for the [Greyskull LP](https://strengthvillain.myshopify.com/collections/all) strength training program. Track your lifts, log your AMRAP sets, and let the app handle progression math automatically.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### Automatic Greyskull LP Progression

The app calculates your next working weight based on standard Greyskull LP rules:

| Performance | Upper Body | Legs |
|---|---|---|
| **10+ reps** on AMRAP set | +2 kg | +4 kg |
| **5-9 reps** on AMRAP set | +1 kg | +2 kg |
| **Under 5 reps** (failed) | -10% deload | -10% deload |

You can always override the suggested weight with a custom value.

### Everything You Need

- **📊 Progress Charts** — Sparkline graphs showing weight progression over time
- **🔢 Plate Calculator** — Shows exactly which plates to load on each side of the bar (20 kg barbell)
- **📅 Date Backfill** — Log workouts from past dates you forgot to track
- **📝 Session Notes** — Attach optional notes to any workout entry
- **🏷️ Exercise Labels** — Organize into Workout A, Workout B, or Supplemental
- **🔍 Filter by Label** — Quick-filter pills on the main dashboard
- **📦 Bulk Operations** — Select multiple exercises for batch deletion
- **⚡ Expandable History** — Shows last 5 entries with a toggle to reveal all
- **🗑️ Undo Last Session** — Remove the most recent log entry with a confirmation step

### Polished UI/UX

- **📱 Mobile-First Design** — Separate optimized templates for mobile and desktop
- **🎨 Warm Color Palette** — Teal, orange, and sage green — easy on the eyes
- **🔔 Toast Notifications** — Auto-dismissing success/error messages
- **🛡️ Double-Submit Protection** — Prevents accidental duplicate logs
- **⏳ Loading States** — Visual feedback during form submissions
- **✨ Smooth Animations** — Cascading fade-ins and transitions throughout

### Data Safety

- **💾 Automatic Backups** — Database backed up after every write operation
- **🔄 Backup Rotation** — Keeps last 10 backups, cleans up older ones automatically
- **🔒 Optional Auth** — HTTP Basic Auth via environment variable (disabled by default)
- **✅ Input Validation** — Server-side validation on all inputs

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/greyskull.git
cd greyskull

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Start the app
python app.py
```

**Windows users** can run the one-click setup script instead:

```powershell
.\start.ps1
```

The app will be available at **http://localhost:5000**

### Migrating from JSON

If you have existing `exercises.json` and `workouts.json` files from a previous version, just place them in the project root. The app will automatically migrate them to SQLite on first startup. Your JSON files are preserved as backup.

---

## ⚙️ Configuration

All configuration is done through a `.env` file. Copy `.env.example` to get started:

```env
# Flask
SECRET_KEY=change-me-to-something-random
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Authentication (leave AUTH_PASSWORD empty to disable)
AUTH_USERNAME=admin
AUTH_PASSWORD=

# Database
DATABASE_PATH=workouts.db

# Backups
BACKUP_DIR=backups
BACKUP_ENABLED=True
```

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `change-me-in-production` | Flask session secret — **change this** |
| `FLASK_DEBUG` | `False` | Enable debug mode (never in production) |
| `FLASK_HOST` | `0.0.0.0` | Bind address |
| `FLASK_PORT` | `5000` | Port number |
| `AUTH_USERNAME` | `admin` | Login username |
| `AUTH_PASSWORD` | *(empty)* | Set a password to enable auth; leave blank to disable |
| `DATABASE_PATH` | `workouts.db` | SQLite database file path |
| `BACKUP_DIR` | `backups` | Where automatic backups are stored |
| `BACKUP_ENABLED` | `True` | Toggle automatic backups |

---

## 🔌 REST API

All endpoints require authentication when `AUTH_PASSWORD` is set. For the web interface a login form is available at `/login` (use the credentials from `AUTH_USERNAME`/`AUTH_PASSWORD`). API clients can still authenticate using standard HTTP Basic auth by supplying the same username/password in the `Authorization` header.

### Exercises

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/exercises` | List all exercises with last workout info |
| `POST` | `/api/exercises` | Create a new exercise |
| `DELETE` | `/api/exercises/<id>` | Delete an exercise and all its history |

### Workouts

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/workout` | Log a workout session |
| `GET` | `/api/history` | Get all workout history |
| `GET` | `/api/exercise-history/<id>` | Get history for a specific exercise |

### Charts

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/exercise-chart/<id>` | SVG line chart of weight over time |

<details>
<summary><strong>Example: Log a workout</strong></summary>

```bash
curl -X POST http://localhost:5000/api/workout \
  -H "Content-Type: application/json" \
  -u admin:yourpassword \
  -d '{
    "exercise_id": "abc12345",
    "weight": 60,
    "reps_category": "more_than_10"
  }'
```

**`reps_category` values:** `less_than_5` | `more_than_5` | `more_than_10`

Optional field: `"custom_next_weight": 65` to override automatic progression.

</details>

<details>
<summary><strong>Example: Add an exercise</strong></summary>

```bash
curl -X POST http://localhost:5000/api/exercises \
  -H "Content-Type: application/json" \
  -u admin:yourpassword \
  -d '{
    "name": "Bench Press",
    "label": "Workout A",
    "exercise_type": "upper",
    "target_reps": 5
  }'
```

**`exercise_type`:** `upper` (plus/minus 1/2 kg increments) or `legs` (plus/minus 2/4 kg increments)

**`label`:** `Workout A` | `Workout B` | `Supplemental`

</details>

---

## 📁 Project Structure

```
greyskull/
├── app.py                  # Flask app — routes, progression logic, chart generation
├── database.py             # SQLAlchemy models, JSON to SQLite migration
├── backup.py               # Standalone backup script (cron / Task Scheduler)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
├── .gitignore
├── start.ps1               # Windows one-click setup and launch
│
├── templates/
│   ├── base.html                              # Shared layout, CSS variables, toast system
│   ├── index.html                             # Desktop exercise dashboard
│   ├── index_mobile.html                      # Mobile exercise dashboard
│   ├── exercise.html                          # Desktop exercise detail and log form
│   ├── exercise_mobile.html                   # Mobile exercise detail and log form
│   ├── exercise_edit.html                     # Desktop edit exercise properties
│   ├── exercise_edit_mobile.html              # Mobile edit exercise properties
│   ├── exercise_delete_confirm.html           # Desktop delete exercise confirmation
│   ├── exercise_delete_confirm_mobile.html    # Mobile delete exercise confirmation
│   ├── exercise_delete_last_confirm.html      # Desktop undo last session confirmation
│   └── exercise_delete_last_confirm_mobile.html  # Mobile undo last session confirmation
│
├── static/css/style.css    # Additional stylesheet
├── instance/workouts.db    # SQLite database (auto-created)
└── backups/                # Auto-rotating database backups
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | [Flask 3.0](https://flask.palletsprojects.com/) + [Flask-SQLAlchemy 3.1](https://flask-sqlalchemy.palletsprojects.com/) |
| **Database** | SQLite — zero config, single file, fully portable |
| **Auth** | [Flask-HTTPAuth 4.8](https://flask-httpauth.readthedocs.io/) (HTTP Basic) |
| **Frontend** | [Bootstrap 5.3](https://getbootstrap.com/) CDN + vanilla JavaScript |
| **Config** | [python-dotenv](https://github.com/theskumar/python-dotenv) |

---

## 💾 Backups

The app automatically backs up the SQLite database after every workout log, edit, or deletion. Backups are stored in the `backups/` directory with timestamps:

```
backups/
├── workouts_backup_20260115_103045.db
├── workouts_backup_20260115_141522.db
└── workouts_backup_20260116_090012.db
```

Only the **10 most recent** backups are kept. Older ones are cleaned up automatically.

You can also run the standalone backup script manually or on a schedule:

```bash
python backup.py
```

**To restore from a backup:** copy a backup file over `instance/workouts.db` and restart the app.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
