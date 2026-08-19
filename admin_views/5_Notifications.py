# pages/4_Notifications.py
import streamlit as st
import pandas as pd
import time
from notifications_engine import dispatch_broadcast, fetch_recent_notifications

# --- Authentication Safety Check ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

# --- Page Setup ---
st.title("🔔 Live Notification & Alert Center")
st.write("Broadcast live system announcements, voting start alerts, and automated reminders.")

# --- Quick Dispatch Presets ---
st.markdown("### ⚡ Fast Trigger Templates")
col_preset1, col_preset2, col_preset3 = st.columns(3)

with col_preset1:
    if st.button("🚀 Broadcast: Polls Are Open!", use_container_width=True, type="primary"):
        dispatch_broadcast(
            title="🗳️ Voting Has Started!", 
            message="Secure voting lines are now open! Cast your vote securely via your registered portal.",
            target_cohort="All Registered Citizens"
        )
        st.toast("Broadcasting: Voting Lines Now OPEN!", icon="🚨")
        time.sleep(1)
        st.rerun()

with col_preset2:
    if st.button("⏰ Broadcast: 1-Hour Reminder", use_container_width=True):
        dispatch_broadcast(
            title="⏳ Reminder: Polls Close Soon", 
            message="Only 1 hour remaining to cast your ballot. Click to access your secure portal.",
            target_cohort="Non-Voters Queue"
        )
        st.toast("Reminder alert dispatched to outstanding non-voters!", icon="📲")
        time.sleep(1)
        st.rerun()

with col_preset3:
    if st.button("✅ Broadcast: Voting Concluded", use_container_width=True):
        dispatch_broadcast(
            title="🔒 Polls Are Closed", 
            message="Voting has officially concluded. Tabulation procedures are now underway.",
            target_cohort="All Citizens"
        )
        st.toast("Closure notice sent successfully.", icon="🔒")
        time.sleep(1)
        st.rerun()

st.divider()

# --- Custom Notification Creator ---
st.markdown("### 📢 Custom Alert Composer")

with st.form("custom_notification_form"):
    title_input = st.text_input("Notification Title", placeholder="e.g., Extended Hours Notice")
    message_input = st.text_area("Notification Body Text", placeholder="Write your announcement message here...")
    cohort_select = st.selectbox(
        "Target Audience Group", 
        ["All Non-Voters", "Cohort 1 (Morning Active)", "Cohort 2 (Afternoon Active)", "Cohort 3 (Evening Active)", "System Admins Only"]
    )
    
    submit_btn = st.form_submit_button("📡 Dispatch Custom Alert")

if submit_btn:
    if title_input and message_input:
        dispatch_broadcast(title_input, message_input, cohort_select)
        st.success(f"Custom alert successfully queued and dispatched to **{cohort_select}**!")
        st.toast(f"Dispatched: {title_input}", icon="📡")
        time.sleep(1)
        st.rerun()
    else:
        st.warning("Please fill in both the title and message fields before sending.")

st.divider()


# --- Live Broadcast Audit History ---

st.markdown ("### 📜 Dispatch Logs & Transmission Audit")



recent_logs = fetch_recent_notifications(limit=10)

if recent_logs:

    log_df = pd.DataFrame(recent_logs, columns=["Alert Title", "Message Preview", "Target Group", "Sent Time", "Status"])
    st.dataframe(log_df, use_container_width=True, hide_index=True)
else:
    st.info("No notifications have been dispatched yet during this session.")