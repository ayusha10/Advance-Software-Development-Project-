# Horizon Cinemas Booking System (HCBS)

Final assessment project: a desktop booking system built with Python and SQLite.

Overview
--------
- Desktop GUI using `tkinter`.
- Layers: Models → Repositories → Services → Controllers → GUI.
- Database: `horizon_db.sqlite3` (schema in `horizon_db.sql`).

Requirements
------------
- Python 3.10 or newer
- No external packages required (standard library only)

Quick start
-----------
1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Create the database (if missing):

```powershell
sqlite3 horizon_db.sqlite3 < horizon_db.sql
```

Or with Python:

```powershell
python - <<'PY'
import sqlite3
sql = open('horizon_db.sql','r',encoding='utf-8').read()
conn = sqlite3.connect('horizon_db.sqlite3')
conn.executescript(sql)
conn.close()
print('horizon_db.sqlite3 created')
PY
```

3. Run the app:

```powershell
python run.py
```

4. Run tests:

```powershell
python run_tests.py
```

Default test accounts
---------------------
- Admin: `admin26` / `admin@2026`
- Manager: `manager26` / `manager@2026`
- Customer: `Customer26` / `customer26`

Files of interest
-----------------
- `run.py` — application entry point
- `run_tests.py` — test runner
- `horizon_db.sql` — DB schema + seed data
- `horizon_db.sqlite3` — runtime database (optional)
- `SUBMISSION_MASTER_ALL.md` — combined submission document

Troubleshooting
---------------
- If `tkinter` import fails, install a Python distribution with Tk support.
- If tests fail, recreate the DB from `horizon_db.sql` and re-run.

License / Notes
----------------
This project is an academic exercise. Remove or change seeded credentials before any public release.

