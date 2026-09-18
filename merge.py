import sqlite3

def merge_votes_and_anomalies():
    # 1. Fetch tables from election_system.db
    conn_sys = sqlite3.connect("election_system.db")
    cursor_sys = conn_sys.cursor()
    
    # Read votes
    cursor_sys.execute("SELECT party_name, region, timestamp FROM votes")
    votes_rows = cursor_sys.fetchall()
    
    # Read anomaly logs
    cursor_sys.execute("SELECT voter_id, anomaly_type, description FROM anomaly_logs")
    anomaly_rows = cursor_sys.fetchall()
    
    conn_sys.close()

    # 2. Insert into election_data.db
    conn_data = sqlite3.connect("election_data.db")
    cursor_data = conn_data.cursor()
    
    # Create and populate votes
    cursor_data.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party_name TEXT,
            region TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor_data.executemany(
        "INSERT INTO votes (party_name, region, timestamp) VALUES (?, ?, ?)", 
        votes_rows
    )
    
    # Create and populate anomaly_logs
    cursor_data.execute("""
        CREATE TABLE IF NOT EXISTS anomaly_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT,
            anomaly_type TEXT,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor_data.executemany(
        "INSERT INTO anomaly_logs (voter_id, anomaly_type, description) VALUES (?, ?, ?)", 
        anomaly_rows
    )

    conn_data.commit()
    conn_data.close()
    
    print(f"✓ Migrated {len(votes_rows)} vote records.")
    print(f"✓ Migrated {len(anomaly_rows)} anomaly log records.")
    print("\n🎉 Success! Both tables are merged into 'election_data.db'.")

if __name__ == "__main__":
    merge_votes_and_anomalies()