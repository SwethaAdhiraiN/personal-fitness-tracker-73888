#!/usr/bin/env python3
"""Initialize SQLite database for workout_database, including users, workout_plans, daily_workouts, body_composition, and progress_tracking tables."""

import sqlite3
import os
from datetime import datetime

DB_NAME = "myapp.db"

print("Starting SQLite setup...")

db_exists = os.path.exists(DB_NAME)
if db_exists:
    print(f"SQLite database already exists at {DB_NAME}")
    # Verify it's accessible
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("SELECT 1")
        conn.close()
        print("Database is accessible and working.")
    except Exception as e:
        print(f"Warning: Database exists but may be corrupted: {e}")
else:
    print("Creating new SQLite database...")

# Create and initialize schema
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

# Table: app_info (meta, unchanged)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS app_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Table: users
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        gender TEXT,
        birthdate DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Table: workout_plans
cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        plan_name TEXT NOT NULL,
        description TEXT,
        start_date DATE NOT NULL,
        end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")

# Table: daily_workouts
cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_plan_id INTEGER NOT NULL,
        workout_date DATE NOT NULL,
        exercise_name TEXT NOT NULL,
        sets INTEGER NOT NULL,
        reps INTEGER NOT NULL,
        weight REAL,
        notes TEXT,
        completed BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(workout_plan_id) REFERENCES workout_plans(id) ON DELETE CASCADE
    )
""")

# Table: body_composition
cursor.execute("""
    CREATE TABLE IF NOT EXISTS body_composition (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        record_date DATE NOT NULL,
        weight REAL NOT NULL,
        body_fat_percentage REAL,
        height REAL,
        waist_circumference REAL,
        other_metrics TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")

# Table: progress_tracking
cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        exercise_name TEXT NOT NULL,
        record_date DATE NOT NULL,
        sets INTEGER,
        reps INTEGER,
        weight REAL,
        volume REAL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")

# Insert initial meta-data
cursor.execute("INSERT OR REPLACE INTO app_info (key, value) VALUES (?, ?)", 
               ("project_name", "workout_database"))
cursor.execute("INSERT OR REPLACE INTO app_info (key, value) VALUES (?, ?)", 
               ("version", "1.0.0"))
cursor.execute("INSERT OR REPLACE INTO app_info (key, value) VALUES (?, ?)", 
               ("author", "John Doe"))
cursor.execute("INSERT OR REPLACE INTO app_info (key, value) VALUES (?, ?)", 
               ("description", "Personal Fitness Tracker Database"))

conn.commit()

# Print table creation summary
cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
table_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM app_info")
record_count = cursor.fetchone()[0]

conn.close()

# Save connection info
current_dir = os.getcwd()
connection_string = f"sqlite:///{current_dir}/{DB_NAME}"
try:
    with open("db_connection.txt", "w") as f:
        f.write(f"# SQLite connection methods:\n")
        f.write(f"# Python: sqlite3.connect('{DB_NAME}')\n")
        f.write(f"# Connection string: {connection_string}\n")
        f.write(f"# File path: {current_dir}/{DB_NAME}\n")
    print("Connection information saved to db_connection.txt")
except Exception as e:
    print(f"Warning: Could not save connection info: {e}")

# Ensure db_visualizer directory and write env
db_path = os.path.abspath(DB_NAME)
if not os.path.exists("db_visualizer"):
    os.makedirs("db_visualizer", exist_ok=True)
    print("Created db_visualizer directory")
try:
    with open("db_visualizer/sqlite.env", "w") as f:
        f.write(f"export SQLITE_DB=\"{db_path}\"\n")
    print(f"Environment variables saved to db_visualizer/sqlite.env")
except Exception as e:
    print(f"Warning: Could not save environment variables: {e}")

print("\nSQLite setup complete!")
print(f"Database: {DB_NAME}")
print(f"Location: {current_dir}/{DB_NAME}")
print("")
print("To use with Node.js viewer, run: source db_visualizer/sqlite.env")
print("\nTo connect to the database, use one of the following methods:")
print(f"1. Python: sqlite3.connect('{DB_NAME}')")
print(f"2. Connection string: {connection_string}")
print(f"3. Direct file access: {current_dir}/{DB_NAME}")
print("")
print("Database statistics:")
print(f"  Tables: {table_count}")
print(f"  App info records: {record_count}")

try:
    import subprocess
    result = subprocess.run(['which', 'sqlite3'], capture_output=True, text=True)
    if result.returncode == 0:
        print("")
        print("SQLite CLI is available. You can also use:")
        print(f"  sqlite3 {DB_NAME}")
except:
    pass

print("\nScript completed successfully.")
