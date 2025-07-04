"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
import sqlite3
from typing import Dict, Any

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
print(f"Current directory: {current_dir}")
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


def get_db_connection():
    conn = sqlite3.connect(os.path.join(current_dir, "activities.db"))
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM activities")
    activities: Dict[str, Any] = {}
    for row in c.fetchall():
        name = row["name"]
        activities[name] = {
            "description": row["description"],
            "schedule": row["schedule"],
            "max_participants": row["max_participants"],
            "participants": []
        }
    # Get participants for each activity
    c.execute("SELECT activity_name, email FROM participants")
    for row in c.fetchall():
        activities[row["activity_name"]]["participants"].append(row["email"])
    conn.close()
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    conn = get_db_connection()
    c = conn.cursor()
    # Check if activity exists
    c.execute("SELECT * FROM activities WHERE name = ?", (activity_name,))
    activity = c.fetchone()
    if not activity:
        conn.close()
        raise HTTPException(status_code=404, detail="Activity not found")
    # Check for duplicate registration
    c.execute("SELECT 1 FROM participants WHERE activity_name = ? AND email = ?", (activity_name, email))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Student already registered for this activity")
    # Add student
    c.execute("INSERT INTO participants (activity_name, email) VALUES (?, ?)", (activity_name, email))
    conn.commit()
    conn.close()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    conn = get_db_connection()
    c = conn.cursor()
    # Check if activity exists
    c.execute("SELECT * FROM activities WHERE name = ?", (activity_name,))
    activity = c.fetchone()
    if not activity:
        conn.close()
        raise HTTPException(status_code=404, detail="Activity not found")
    # Check if participant is registered
    c.execute("SELECT 1 FROM participants WHERE activity_name = ? AND email = ?", (activity_name, email))
    if not c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Student not registered for this activity")
    # Remove participant
    c.execute("DELETE FROM participants WHERE activity_name = ? AND email = ?", (activity_name, email))
    conn.commit()
    conn.close()
    return {"message": f"Unregistered {email} from {activity_name}"}
