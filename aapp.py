import streamlit as st

# Setup global page configurations
st.set_page_config(page_title="Election Security Portal", page_icon="🛡️", layout="wide")

# Step 1: Initialize session state variable if not present
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Step 2: Create a login view function
def login_screen():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.write("## 🛡️ Admin Entry Gate")
        with st.container(border=True):
            st.write("### Sign In")
            with st.form("login_form", border=False):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Authenticate", use_container_width=True)
                
                if submit:
                    # In production, check these against a secure database
                    if username == "admin" and password == "secure2026":
                        st.session_state["authenticated"] = True
                        st.success("Access Granted.")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

# Step 3: Map Pages
login_page = st.Page(login_screen, title="Login", icon="🔒")
dashboard = st.Page("admin_views/1_Dashboard.py", title="Live Telemetry", icon="📊")

# Step 4: Define Dynamic Navigation
if not st.session_state["authenticated"]:
    # Restricts unauthorized users strictly to the login interface (prevents URL bypass)
    pg = st.navigation([login_page], position="hidden")
    pg.run()
else:
    pg = st.navigation({"OVERVIEW": [dashboard]})
    with st.sidebar:
        if st.button("Log Out"):
            st.session_state["authenticated"] = False
            st.rerun()
    pg.run()
