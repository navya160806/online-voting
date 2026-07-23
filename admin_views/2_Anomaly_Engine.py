import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# --- Security Access Control ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

st.title("🛡️ Automated Threat Guard & Security Center")
st.write("Real-time automated security monitoring and single-click incident containment.")

# --- Background Telemetry Generation ---
@st.cache_data
def load_telemetry():
    np.random.seed(42)
    normal = np.random.normal(loc=[120, 2, 45], scale=[15, 1, 8], size=(300, 3))
    anomalies = np.random.uniform(low=[250, 8, 120], high=[600, 20, 350], size=(15, 3))
    botnet = np.random.normal(loc=[400, 12, 180], scale=[10, 0.5, 5], size=(20, 3))
    
    data = np.vstack([normal, anomalies, botnet])
    df = pd.DataFrame(data, columns=["Latency (ms)", "Proxy Hops", "Payload Size (KB)"])
    df["Session_ID"] = [f"SESS_{i:04d}" for i in range(len(df))]
    return df

df = load_telemetry()

# --- Automated Machine Learning Diagnostics (Runs completely behind the scenes) ---
# 1. Detect Individual Hackers (Isolation Forest)
iso = IsolationForest(contamination=0.05, random_state=42)
df["Is_Outlier"] = iso.fit_predict(df[["Latency (ms)", "Proxy Hops", "Payload Size (KB)"]])

# 2. Detect Group Botnet Attacks (DBSCAN)
scaler = StandardScaler()
scaled_vals = scaler.fit_transform(df[["Latency (ms)", "Proxy Hops", "Payload Size (KB)"]])
db = DBSCAN(eps=0.5, min_samples=5)
df["Group_Cluster"] = db.fit_predict(scaled_vals)

# Summarize metrics for the Admin
flagged_outliers = df[df["Is_Outlier"] == -1]
botnet_clusters = df[df["Group_Cluster"] >= 0]
total_threats = len(flagged_outliers)

# ==========================================
# 1. EXECUTIVE STATUS BANNER
# ==========================================
st.markdown("### 🚦 Overall Security Posture")

col_gauge, col_stats = st.columns([1, 2])

with col_gauge:
    # Easy gauge chart: Green = Good, Red = Bad
    threat_level = min(100, int((total_threats / len(df)) * 500))
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=threat_level,
        title={'text': "System Risk Index"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#EF4444" if threat_level > 30 else "#10B981"},
            'steps': [
                {'range': [0, 30], 'color': "#D1FAE5"},
                {'range': [30, 70], 'color': "#FEF3C7"},
                {'range': [70, 100], 'color': "#FEE2E2"}
            ]
        }
    ))
    fig_gauge.update_layout(height=220, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_stats:
    st.write(" ")
    if threat_level < 30:
        st.success("✅ **SYSTEM HEALTHY:** Normal activity patterns detected across all nodes.")
    else:
        st.error("⚠️ **ATTENTION REQUIRED:** Automated ML models detected suspicious traffic spikes.")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Active Sessions", len(df))
    m2.metric("Flagged Threats", total_threats, delta=f"{total_threats} alerts", delta_color="inverse")
    m3.metric("Botnet Groups", len(botnet_clusters["Group_Cluster"].unique()))

st.divider()

# ==========================================
# 2. ACTIONABLE INCIDENT TABLE & MITIGATION
# ==========================================
st.markdown("### 🎯 Active Security Threats & Rapid Action")
st.caption("Review flagged suspicious traffic below and execute automated containment actions.")

# Filter only bad sessions
threat_df = df[(df["Is_Outlier"] == -1) | (df["Group_Cluster"] >= 0)].copy()
threat_df["Threat Type"] = np.where(
    threat_df["Group_Cluster"] >= 0, "🤖 Coordinated Botnet", "🚨 Suspicious Lone Outlier"
)

# Render clean, simple 2D Chart non-technical people can read instantly
fig_simple = px.scatter(
    threat_df,
    x="Latency (ms)",
    y="Payload Size (KB)",
    color="Threat Type",
    hover_data=["Session_ID", "Proxy Hops"],
    title="Flagged Threats Overview (High Response Time vs Payload Size)",
    color_discrete_map={"🤖 Coordinated Botnet": "#EF4444", "🚨 Suspicious Lone Outlier": "#F59E0B"}
)
st.plotly_chart(fig_simple, use_container_width=True)

# Table display with simple click actions
st.write("#### Flagged Session Log")

# Format for clean display
display_df = threat_df[["Session_ID", "Threat Type", "Latency (ms)", "Proxy Hops", "Payload Size (KB)"]]
st.dataframe(display_df, use_container_width=True, hide_index=True)

# One-Click Action Center
st.markdown("#### ⚡ Automated Action Response")
col_act1, col_act2 = st.columns([2, 1])

with col_act1:
    selected_session = st.selectbox("Select Session to Contain:", threat_df["Session_ID"].unique())

with col_act2:
    st.write(" ")
    st.write(" ")
    if st.button("🔒 Isolate & Block Session", type="primary"):
        st.toast(f"✅ Session {selected_session} has been blocked and revoked from the network!", icon="🛡️")
        st.success(f"Action Executed: Firewall rule created for {selected_session}.")