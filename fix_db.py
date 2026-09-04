import sqlite3

conn = sqlite3.connect("election_system.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE voters ADD COLUMN has_voted INTEGER DEFAULT 0;")
    conn.commit()
    print("Column 'has_voted' added successfully!")
except sqlite3.OperationalError as e:
    print("Error or column already exists:", e)

conn.close()