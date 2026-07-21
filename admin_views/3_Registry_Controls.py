import streamlit as st
import pandas as pd
import streamlit as st

# Safety check: Initialize the key if Streamlit pre-runs this file out of order
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

st.title("👥 Voter Registry & Verification Holds")
st.write("Review active signature integrity queues and override automated engine flags.")

# Instantiate database session state dictionary if empty
if "voter_db" not in st.session_state:
    st.session_state["voter_db"] = pd.DataFrame([
        {"Voter ID": "V-10294", "Name": "Marcus Vance", "Precinct": "Region 4", "Signature Match": "65%", "Status": "Verification Hold"},
        {"Voter ID": "V-14920", "Name": "Elena Rostova", "Precinct": "Region 2", "Signature Match": "94%", "Status": "Verified Approved"},
        {"Voter ID": "V-11841", "Name": "David Kene", "Precinct": "Region 4", "Signature Match": "42%", "Status": "Auto-Flagged Threat"},
        {"Voter ID": "V-19402", "Name": "Siddharth Nair", "Precinct": "Region 1", "Signature Match": "68%", "Status": "Verification Hold"}
    ])

# Quick Filters
status_filter = st.selectbox("Filter Status Queue", ["All Records", "Verification Hold", "Verified Approved", "Auto-Flagged Threat"])
filtered_df = st.session_state["voter_db"] if status_filter == "All Records" else st.session_state["voter_db"][st.session_state["voter_db"]["Status"] == status_filter]

st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.write("---")
st.subheader("🛠️ Administrative Override Panel")

col1, col2, col3 = st.columns(3)
with col1:
    target_voter = st.selectbox("Target Voter ID", st.session_state["voter_db"]["Voter ID"].tolist())
with col2:
    new_action = st.selectbox("Apply Override Decision Action", ["Verified Approved", "Rejected Fraudulent", "Verification Hold"])
with col3:
    st.write("<br>", unsafe_allow_html=True) # Vertical alignment balance
    if st.button("Execute Override Action", use_container_width=True, type="primary"):
        # Update row dynamically in session data
        st.session_state["voter_db"].loc[st.session_state["voter_db"]["Voter ID"] == target_voter, "Status"] = new_action
        st.success(f"Record {target_voter} updated to status: {new_action}")
        st.timer(1.5)
        st.rerun()