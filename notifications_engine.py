# notifications_engine.py
import sqlite3
from datetime import datetime

DB_PATH = "voting_system.db"

def init_notification_db():
    """Ensure notification tracking table exists inside SQLite."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notification_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            message TEXT,
            target_cohort TEXT,
            sent_at TIMESTAMP,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def dispatch_broadcast(title, message, target_cohort="All Non-Voters"):
    """
    Simulates sending targeted SMS/Push notifications and logs the entry.
    """
    init_notification_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO notification_logs (title, message, target_cohort, sent_at, status)
        VALUES (?, ?, ?, ?, ?)
    """, (title, message, target_cohort, timestamp, "DELIVERED"))
    
    conn.commit()
    conn.close()
    return True

def fetch_recent_notifications(limit=10):
    """Retrieve history of sent broadcasts."""
    init_notification_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, message, target_cohort, sent_at, status 
        FROM notification_logs 
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows