import sqlite3

# Pre-populated activities data
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in local leagues",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": []
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Drama Club": {
        "description": "Participate in school plays and improve acting skills",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
    }
}

def init_db():
    conn = sqlite3.connect("activities.db")
    c = conn.cursor()
    # Create activities table
    c.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            name TEXT PRIMARY KEY,
            description TEXT,
            schedule TEXT,
            max_participants INTEGER
        )
    """)
    # Create participants table
    c.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            activity_name TEXT,
            email TEXT,
            PRIMARY KEY (activity_name, email),
            FOREIGN KEY (activity_name) REFERENCES activities(name)
        )
    """)
    # Insert activities and participants
    for name, details in activities.items():
        c.execute("""
            INSERT OR REPLACE INTO activities (name, description, schedule, max_participants)
            VALUES (?, ?, ?, ?)
        """, (name, details["description"], details["schedule"], details["max_participants"]))
        for email in details["participants"]:
            c.execute("""
                INSERT OR IGNORE INTO participants (activity_name, email)
                VALUES (?, ?)
            """, (name, email))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()

