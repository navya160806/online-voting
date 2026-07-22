import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import streamlit as st

# Safety check: Initialize the key if Streamlit pre-runs this file out of order
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

st.title("📡 Unsupervised ML Threat Diagnostics")
st.write("Real-time zero-day exploit mapping using multi-dimensional spatial clustering.")

# Generate mock telemetry logs (Request Latency, Session Hop Count, Input Payload Size)
@st.cache_data
def generate_telemetry_data():
    np.random.seed(42)
    normal = np.random.normal(loc=[120, 2, 45], scale=[15, 1, 8], size=(300, 3))
    anomalies = np.random.uniform(low=[250, 8, 120], high=[600, 20, 350], size=(15, 3))
    botnet_cluster_1 = np.random.normal(loc=[400, 12, 180], scale=[10, 0.5, 5], size=(20, 3))
    
    data = np.vstack([normal, anomalies, botnet_cluster_1])
    return pd.DataFrame(data, columns=["Latency (ms)", "Proxy Hops", "Payload Size (KB)"])

df = generate_telemetry_data()

tab1, tab2 = st.tabs(["Individual Session Outliers", "Botnet Coordination Clustering"])

with tab1:
    st.subheader("Isolation Forest Anomaly Isolation")
    contamination = st.slider("Target Contamination Budget Rate", 0.01, 0.15, 0.05)
    
    # Run Isolation Forest Engine
    iso_model = IsolationForest(contamination=contamination, random_state=42)
    df["Anomaly_Score"] = iso_model.fit_predict(df[["Latency (ms)", "Proxy Hops", "Payload Size (KB)"]])
    df["Status"] = df["Anomaly_Score"].map({1: "Normal Baseline", -1: "Flagged Threat Profile"})
    
    fig_iso = px.scatter_3d(
        df, x="Latency (ms)", y="Proxy Hops", z="Payload Size (KB)",
        color="Status", color_discrete_map={"Normal Baseline": "#3B82F6", "Flagged Threat Profile": "#EF4444"},
        opacity=0.7, title="Isolation Space Vector Map"
    )
    st.plotly_chart(fig_iso, use_container_width=True)

with tab2:
    st.subheader("DBSCAN Coordinate Threat Spatial Grouping")
    eps = st.slider("Epsilon Neighborhood Density Threshold (eps)", 10.0, 50.0, 25.0)
    min_samples = st.slider("Minimum Cluster Sample Core Requirement", 3, 15, 5)
    
    # Run DBSCAN Engine
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    df["Cluster"] = dbscan.fit_predict(df[["Latency (ms)", "Proxy Hops", "Payload Size (KB)"]])
    df["Cluster_Label"] = df["Cluster"].apply(lambda x: f"Botnet Profile #{x}" if x != -1 else "Unstructured Scatter")
    
    fig_db = px.scatter_3d(
        df, x="Latency (ms)", y="Proxy Hops", z="Payload Size (KB)",
        color="Cluster_Label", title="Density-Based Spatial Threat Clusters"
    )
    st.plotly_chart(fig_db, use_container_width=True)