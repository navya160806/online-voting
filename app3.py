import streamlit as st
import base64

# 1. Global Page Parameters (Must be the very first Streamlit command)
st.set_page_config(
    page_title="Secure Election Admin Console",
    page_icon="🛡️",
    layout="wide"
)

# 2. Initialization: Check authorization states immediately
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def render_login_view():
    try:
        with open("static/video/login.mp4", "rb") as video_file:
            video_bytes = video_file.read()
        base64_video = base64.b64encode(video_bytes).decode("utf-8")
        
        st.markdown(f"""
            <style>
                #bg-video {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    z-index: -100;
                    object-fit: cover;
                    filter: brightness(40%) contrast(110%);
                }}
                .stApp, [data-testid="stAppViewMain"], [data-testid="stHeader"], .stMainBlockContainer {{
                    background-color: transparent !important;
                    background: transparent !important;
                    overflow: hidden;
                }}
                .login-header {{
                    color: #FFFFFF !important;
                    text-shadow: 0px 4px 12px rgba(0, 0, 0, 0.8);
                }}
                [data-testid="stForm"] {{
                    background-color: rgba(255, 255, 255, 0.95) !important;
                    border-radius: 12px;
                    padding: 20px 25px 35px 25px !important;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
                }}
                [data-testid="stForm"] label {{
                    color: #1A202C !important;
                    font-weight: 500;
                }}
            </style>
            <video autoplay loop muted playsinline id="bg-video">
                <source src="data:video/mp4;base64,{base64_video}" type="video/mp4">
            </video>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.markdown("""
            <style>
                .stApp { background-color: #0B0F17; }
                .login-header { color: #FFFFFF !important; }
            </style>
        """, unsafe_allow_html=True)

    st.write("<br><br><br>", unsafe_allow_html=True)
    left_gap, center_card, right_gap = st.columns([1, 1.2, 1])
    
    with center_card:
        st.markdown("<h2 class='login-header'>🛡️ Admin Security Gate</h2>", unsafe_allow_html=True)
        
        with st.container(border=True):
            with st.form("admin_login_form", border=False):
                username = st.text_input("Administrator Identifier", placeholder="e.g., admin")
                password = st.text_input("Access Passkey", type="password", placeholder="••••••••")
                submit_button = st.form_submit_button("Request Mainframe Access", use_container_width=True)
                
                if submit_button:
                    if username == "admin" and password == "secure2026":
                        st.session_state["authenticated"] = True
                        st.rerun()
                    else:
                        st.error("Authentication Denied.")

# 4. Page Routing Definitions
login_page = st.Page(render_login_view, title="Security Gate", icon="🔒")
dashboard = st.Page("admin_views/12_dashboard.py", title="Live Telemetry Dashboard", icon="📊", default=True)
anomaly_eng = st.Page("admin_views/2_Anomaly_Engine.py", title="ML Threat Diagnostics", icon="📡")
registry = st.Page("admin_views/3_Registry_Controls.py", title="Voter Registry & Hold Queue", icon="👥")
rag_desk = st.Page("admin_views/4_RAG_Legal_Desk.py", title="AI Legal & SOP Command", icon="🤖")

# 5. Routing Execution Logic
if not st.session_state["authenticated"]:
    pg = st.navigation([login_page], position="hidden")
else:
    pg = st.navigation({
        "OVERVIEW": [dashboard],
        "CYBER DIAGNOSTICS": [anomaly_eng],
        "DATABASE ADMINISTRATION": [registry],
        "DECISION ASSISTANCE": [rag_desk]
    })
    
    # Render logout button cleanly at the base of the sidebar
    with st.sidebar:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Disconnect Session", key="sidebar_logout_btn", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

pg.run()