# Workout Database

This directory provides the SQLite database for the Personal Fitness Tracker application, including schema setup, manual shell, testing, and a lightweight database visualizer.

## Overview

- **Purpose:** Stores user accounts, workout plans, daily workouts, body composition, and progress tracking.
- **Database:** SQLite file (`myapp.db`).
- **Includes:**
  - DB schema/init scripts
  - Test/validation utilities
  - Database shell (`db_shell.py`)
  - Optional JavaScript-based visualizer (`db_visualizer/`)

## Environment Variables

- None required for core SQLite operations. (SQLite stores the DB as a file: `myapp.db`)
- For the Node.js visualizer:  
  Set `SQLITE_DB` via env file (`db_visualizer/sqlite.env` is created by init script):

    ```
    export SQLITE_DB="/full/path/to/myapp.db"
    ```

## Bootstrapping

Run all commands from this directory unless noted otherwise.

### 1. Install Requirements

- Python ≥ 3.7 required for shell/scripts.
- *Node.js is only required to use the optional db_visualizer.*

### 2. Initialize Database

Creates `myapp.db` (if not already present), applies schema, and stores connection info:

```sh
python3 init_db.py
```

- This script will also generate:
    - `db_connection.txt` (ready-to-use connection string)
    - `db_visualizer/sqlite.env` with the DB file path

### 3. Optional: Test Database

Verify DB exists and is accessible:

```sh
python3 test_db.py
```

### 4. Use Database Shell

Interactive SQLite shell for testing queries:
```sh
python3 db_shell.py
```

#### DB Schema

See `init_db.py` for all tables:
- users
- workout_plans
- daily_workouts
- body_composition
- progress_tracking

### 5. Optional: Database Visualizer

A Node.js based viewer supporting SQLite, Postgres, MySQL, MongoDB (run with SQLite for this project):

```sh
cd db_visualizer
npm install
# Set up environment variable with SQLite file location if not set:
source sqlite.env
npm start
```
Open http://localhost:3000 to browse database content.

## Container Integration

- **Backend** (Django) expects the SQLite DB file to be placed at a known path.
- For local/dev, ensure the backend reads the same DB:
    - Either copy/set `myapp.db` in the backend container/workspace, or
    - Use a shared/mounted volume, or
    - Set the `SQLITE_DB` env variable in the backend container to point to the path of `myapp.db`.
- The backend will automatically detect `SQLITE_DB` if set (see backend/config/settings.py).

### Example Cross-Container Setup

- Initialize database _first_ (in this directory).
- Set env variable `SQLITE_DB` in backend (via .env or OS env) to match the file path.
- Launch backend (API) server.
- Launch frontend (provides UI).
- Optionally run db_visualizer as needed.

## Known Ports

- SQLite: File-based, no listening port
- Database Visualizer (Node.js): **3000**

## Notes

- Make sure the backend _and_ visualizer (if used) point to the same `myapp.db` for consistent data.
- No migrations are necessary here; schema is controlled by `init_db.py`.

## Contact & Help

For further troubleshooting or advanced migration, refer to `init_db.py` and `db_shell.py` source files.
