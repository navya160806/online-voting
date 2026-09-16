import sqlite3
import random
from datetime import datetime, timedelta

DB_NAME = "election_system.db"

# Sample data generators
FIRST_NAMES = ["Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Neha", "Rahul", "Pooja", "Amit", "Sanya", 
               "Karan", "Riya", "Aditya", "Kavya", "Siddharth", "Ishita", "Arjun", "Sneha", "Varun", "Meera"]
LAST_NAMES = ["Sharma", "Verma", "Singh", "Gupta", "Kumar", "Patel", "Reddy", "Nair", "Joshi", "Rao", 
              "Mehta", "Chawla", "Agarwal", "Mishra", "Pandey", "Deshmukh", "Iyer", "Banerjee", "Roy", "Khan"]
REGIONS = ["Uttar Pradesh", "Maharashtra", "Delhi NCR", "Karnataka", "West Bengal"]
PARTIES = ["Progressive Alliance (PA)", "Democratic Coalition (DC)", "National Reform Front (NRF)"]
ANOMALY_TYPES = [
    ("DUPLICATE_REGISTRATION", "Attempted to register existing Voter ID again."),
    ("UNREGISTERED_VOTE_ATTEMPT", "Unregistered voter ID attempted to cast a ballot."),
    ("DOUBLE_VOTE_ATTEMPT", "Voter attempted to cast a second vote.")
]

def seed_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Ensure tables exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voters (
            voter_id TEXT PRIMARY KEY,
            full_name TEXT,
            region TEXT,
            age INTEGER,
            has_voted INTEGER DEFAULT 0,
            registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            party_name TEXT,
            region TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anomaly_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_id TEXT,
            anomaly_type TEXT,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    print("Generating 220 mock voters...")
    voters_data = []
    votes_data = []
    
    # Generate 220 voters
    for i in range(1, 221):
        voter_id = f"EPIC{1000000 + i}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        region = random.choice(REGIONS)
        age = random.randint(18, 75)
        
        # ~65% of registered voters have cast their vote
        has_voted = 1 if random.random() < 0.65 else 0
        
        # Calculate random registration timestamp in the last 7 days
        reg_time = datetime.now() - timedelta(days=random.randint(1, 7), minutes=random.randint(0, 1440))
        reg_time_str = reg_time.strftime("%Y-%m-%d %H:%M:%S")

        voters_data.append((voter_id, name, region, age, has_voted, reg_time_str))

        # If voter has voted, assign a random vote entry weighted across parties
        if has_voted == 1:
            # Weighted distribution (PA: 45%, DC: 35%, NRF: 20%)
            party = random.choices(PARTIES, weights=[45, 35, 20], k=1)[0]
            vote_time = reg_time + timedelta(hours=random.randint(1, 12))
            votes_data.append((party, region, vote_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Insert Voters
    cursor.executemany("""
        INSERT OR REPLACE INTO voters (voter_id, full_name, region, age, has_voted, registration_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, voters_data)

    # Insert Votes Cast
    cursor.executemany("""
        INSERT INTO votes (party_name, region, timestamp)
        VALUES (?, ?, ?)
    """, votes_data)

    # 2. Generate Anomaly Security Logs
    print("Generating mock anomaly security logs...")
    anomaly_data = []
    for _ in range(15):
        anom_type, desc = random.choice(ANOMALY_TYPES)
        rand_voter = f"EPIC{random.randint(1000001, 1000220)}"
        anom_time = datetime.now() - timedelta(hours=random.randint(1, 48))
        anomaly_data.append((rand_voter, anom_type, desc, anom_time.strftime("%Y-%m-%d %H:%M:%S")))

    cursor.executemany("""
        INSERT INTO anomaly_logs (voter_id, anomaly_type, description, timestamp)
        VALUES (?, ?, ?, ?)
    """, anomaly_data)

    conn.commit()
    conn.close()
    print("Database populated successfully with 220 voters, vote tallies, and security logs!")

if __name__ == "__main__":
    seed_database()