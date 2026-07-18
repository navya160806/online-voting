import streamlit as st

# 1. Global Page Parameters (Must be the very first Streamlit command)
st.set_page_config(
    page_title="Secure Election Admin Console",
    page_icon="🛡️",
    layout="wide"
)

# 2. Initialize tracking states
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 3. Create the Login View Function
def render_login_view():
    left_gap, center_card, right_gap = st.columns([1, 1.2, 1])
    with center_card:
        st.write("## 🛡️ Admin Security Gate")
        st.write("Please authenticate to access the live voting telemetry system.")
        
        with st.container(border=True):
            st.write("### Sign In")
            with st.form("admin_login_form", border=False):
                username = st.text_input("Administrator Identifier", placeholder="e.g., admin")
                password = st.text_input("Access Passkey", type="password", placeholder="••••••••")
                
                st.write("") 
                submit_button = st.form_submit_button("Request Mainframe Access", use_container_width=True)
                
                if submit_button:
                    if username == "admin" and password == "secure2026":
                        st.session_state["authenticated"] = True
                        st.success("Access Granted! Initializing command routing...")
                        st.rerun() # Forces Streamlit to instantly redraw the screen with the new menu
                    else:
                        st.error("Authentication Denied: Invalid credentials.")

# 4. Define ALL Page Layout Modules
login_page = st.Page(render_login_view, title="Security Gate", icon="🔒")

dashboard = st.Page("admin_views/1_Dashboard.py", title="Live Telemetry Dashboard", icon="📊", default=True)
anomaly_eng = st.Page("admin_views/2_Anomaly_Engine.py", title="ML Threat Diagnostics", icon="📡")
registry = st.Page("admin_views/3_Registry_Controls.py", title="Voter Registry & Hold Queue", icon="👥")
rag_desk = st.Page("admin_views/4_RAG_Legal_Desk.py", title="AI Legal & SOP Command", icon="🤖")

# 5. DYNAMIC ROUTING ENGINE (The Security Firewall)
if not st.session_state["authenticated"]:
    # FORCE ONLY LOGIN SCREEN: The sidebar pages physically do not exist in memory yet
    pg = st.navigation([login_page], position="hidden")
else:
    # REVEAL ALL PAGES: Build out the entire categorized sidebar dynamically
    pg = st.navigation({
        "OVERVIEW": [dashboard],
        "CYBER DIAGNOSTICS": [anomaly_eng],
        "DATABASE ADMINISTRATION": [registry],
        "DECISION ASSISTANCE": [rag_desk]
    })
    
    # Render a clean secure sign-out button at the bottom of the sidebar
    with st.sidebar:
        st.write("---")
        if st.button("Disconnect Session", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun() # Instantly locks down the app and brings back the login wall

# Run the selected page router
pg.run()