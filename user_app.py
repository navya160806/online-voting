import streamlit as st
import sqlite3

st.set_page_config(page_title="Public Voter Portal", page_icon="🗳️", layout="centered")

DB_NAME = "election_system.db"

# -------------------------------------------------------------------
# DATABASE INITIALIZATION (Auto-creates missing tables)
# -------------------------------------------------------------------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        
        # Table 1: Registered Voters
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
        
        # Table 2: Cast Votes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                party_name TEXT,
                region TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table 3: Anomaly & Security Logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anomaly_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id TEXT,
                anomaly_type TEXT,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# Ensure tables exist when user_app.py starts
init_db()

# -------------------------------------------------------------------
# DATABASE HELPER FUNCTIONS
# -------------------------------------------------------------------
def get_voter(voter_id):
    """Retrieve voter record by ID."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT voter_id, full_name, region, age, has_voted FROM voters WHERE voter_id = ?", (voter_id,))
        return cursor.fetchone()

def register_voter(voter_id, full_name, region, age):
    """Register a new voter profile prior to voting."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO voters (voter_id, full_name, region, age, has_voted) VALUES (?, ?, ?, ?, 0)",
                (voter_id, full_name, region, age)
            )
            conn.commit()
            return True, "Registration successful! You can now proceed to vote."
        except sqlite3.IntegrityError:
            # Trigger Anomaly: Duplicate Registration Attempt
            cursor.execute(
                "INSERT INTO anomaly_logs (voter_id, anomaly_type, description) VALUES (?, ?, ?)",
                (voter_id, "DUPLICATE_REGISTRATION", f"Attempted to register existing Voter ID '{voter_id}' again.")
            )
            conn.commit()
            return False, "This Voter ID is already registered."

def cast_vote(voter_id, party_choice):
    """Validate and record a vote."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT region, has_voted FROM voters WHERE voter_id = ?", (voter_id,))
        record = cursor.fetchone()

        # Anomaly Check 1: Unregistered ID
        if not record:
            cursor.execute(
                "INSERT INTO anomaly_logs (voter_id, anomaly_type, description) VALUES (?, ?, ?)",
                (voter_id, "UNREGISTERED_VOTE_ATTEMPT", f"Unregistered ID '{voter_id}' tried to cast a vote.")
            )
            conn.commit()
            return False, "Voter ID not recognized. Please register first under Step 1."

        region, has_voted = record

        # Anomaly Check 2: Double Voting Attempt
        if has_voted == 1:
            cursor.execute(
                "INSERT INTO anomaly_logs (voter_id, anomaly_type, description) VALUES (?, ?, ?)",
                (voter_id, "DOUBLE_VOTE_ATTEMPT", f"Voter '{voter_id}' attempted to cast a 2nd vote for '{party_choice}'.")
            )
            conn.commit()
            return False, "Security Notice: You have already cast your vote!"

        # Process valid vote
        cursor.execute("INSERT INTO votes (party_name, region) VALUES (?, ?)", (party_choice, region))
        cursor.execute("UPDATE voters SET has_voted = 1 WHERE voter_id = ?", (voter_id,))
        conn.commit()
        return True, "Your vote has been cast and recorded securely."

# -------------------------------------------------------------------
# USER INTERFACE LAYOUT
# -------------------------------------------------------------------
st.title("🗳️ Public Voter Interface")
st.markdown("Register your details to create your identity, then cast your ballot securely.")

tab1, tab2 = st.tabs(["📝 Step 1: Pre-Election Voter Registration", "🗳️ Step 2: Digital Voting Booth"])

# -------------------------------------------------------------------
# STEP 1: VOTER REGISTRATION FORM
# -------------------------------------------------------------------
with tab1:
    st.subheader("Voter Profile Setup")
    st.info("Complete this form prior to Election Day to create your identity in the electoral roll.")

    with st.form("user_registration_form"):
        voter_id_input = st.text_input("Voter ID Card Number (e.g., EPIC9876543)").strip()
        full_name_input = st.text_input("Full Name").strip()
        region_input = st.selectbox("Select State / Constituency", [
            "Uttar Pradesh", "Maharashtra", "Delhi NCR", "Karnataka", "West Bengal", "Other"
        ])
        age_input = st.number_input("Age", min_value=18, max_value=120, value=25)
        
        submit_reg = st.form_submit_button("Complete Registration")

    if submit_reg:
        if not voter_id_input or not full_name_input:
            st.warning("Please fill out both your Voter ID and Full Name.")
        else:
            success, msg = register_voter(voter_id_input, full_name_input, region_input, age_input)
            if success:
                st.success(msg)
            else:
                st.error(msg)

# -------------------------------------------------------------------
# STEP 2: DIGITAL VOTING BOOTH
# -------------------------------------------------------------------
with tab2:
    st.subheader("Official Digital Voting Booth")
    
    auth_id = st.text_input("Enter Registered Voter ID to Access Ballot", key="vote_auth_input").strip()

    if auth_id:
        voter_record = get_voter(auth_id)

        if voter_record:
            v_id, name, region, age, has_voted = voter_record

            if has_voted == 1:
                st.warning(f"⚠️ **{name}** ({v_id}) has already submitted a vote. Multiple votes are restricted.")
            else:
                st.success(f"Identity Verified: **{name}** | Region: **{region}**")
                
                party_choice = st.radio(
                    "Select Party / Candidate:",
                    [
                        "Progressive Alliance (PA)",
                        "Democratic Coalition (DC)",
                        "National Reform Front (NRF)"
                    ]
                )

                if st.button("Submit Vote"):
                    success, msg = cast_vote(v_id, party_choice)
                    if success:
                        st.balloons()
                        st.success(msg)
                    else:
                        st.error(msg)
        else:
            st.error("Voter ID not found in system. Please register under Step 1 first.")