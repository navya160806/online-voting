import streamlit as st
import pandas as pd
import sqlite3
import os

DB_NAME = "election_data.db"

def run_query(query, params=()):
    """Run read-only query against existing SQLite database."""
    if not os.path.exists(DB_NAME):
        
        st.error(f"❌ Database file '{DB_NAME}' not found at path.")
        return pd.DataFrame()
    try:
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Database Query Error: {e}")
        return pd.DataFrame()

# Check what tables actually exist in your database file
tables_df = run_query("SELECT name FROM sqlite_master WHERE type='table';")

if not tables_df.empty:
    existing_tables = tables_df["name"].tolist()
    st.write("📁 **Tables found in your existing database:**", existing_tables)
    
    # Select the table you want to display
    selected_table = st.selectbox("Select Table to View Real Data:", existing_tables)
    
    # Fetch existing data from the selected table
    df_existing = run_query(f"SELECT * FROM {selected_table}")

    
    st.subheader(f"📊 Real Data from `{selected_table}`")
    if not df_existing.empty:
        st.dataframe(df_existing, use_container_width=True)
    else:
        st.info(f"The table `{selected_table}` exists but currently contains no records.")
else:
    st.error("No tables were found in the connected database file.")