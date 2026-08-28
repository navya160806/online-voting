import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

# Path to your EXISTING database file
DB_NAME = "election_data.db"  # Change to "election_data.db" if needed

def run_query(query, params=()):
    """Run read-only query against existing SQLite database."""
    if not os.path.exists(DB_NAME):
        st.error(f"❌ Database file '{DB_NAME}' not found.")
        return pd.DataFrame()
    try:
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Database Query Error: {e}")
        return pd.DataFrame()

def block_session_in_db(session_id):
    """Update status of a flagged session directly in the existing database."""
    try:
        row_id = int(session_id.replace("SESS_", ""))
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE threats_log SET alert_color = 'BLOCKED' WHERE rowid = ?", (row_id,))
            conn.commit()
    except Exception as e:
        st.error(f"Failed to update session record: {e}")

# Security Access Control
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = True

if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

st.title("🛡️ Automated Threat Guard & Security Center")
st.write("Real-time security telemetry connected directly to existing database logs.")

def fetch_telemetry_data():
    # Inspect column names in the existing threats_log table to avoid SQL missing column errors
    columns_df = run_query("PRAGMA table_info(threats_log)")
    if columns_df.empty:
        st.warning("⚠️ Table 'threats_log' does not exist in the connected database.")
        return pd.DataFrame()

    existing_cols = columns_df["name"].tolist()
    
    # Query only columns that actually exist in your database table
    select_cols = ["rowid as Session_ID"]
    for col in ["timestamp", "alert_color", "details", "latency", "proxy_hops", "payload_size"]:
        if col in existing_cols:
            select_cols.append(col)
            
    query = f"SELECT {', '.join(select_cols)} FROM threats_log"
    if "alert_color" in existing_cols:
        query += " WHERE alert_color != 'BLOCKED' OR alert_color IS NULL"

    df = run_query(query)
    if df.empty:
        return pd.DataFrame()

    def extract_metrics(row):
        lat = row.get("latency", 0) if "latency" in existing_cols else 0
        hops = row.get("proxy_hops", 0) if "proxy_hops" in existing_cols else 0
        p_size = row.get("payload_size", 0) if "payload_size" in existing_cols else 0
        
        # If dedicated metric columns don't exist or equal zero, parse the text inside 'details'
        if (lat == 0 and hops == 0 and p_size == 0) and ("details" in existing_cols) and pd.notna(row.get("details")):
            try:
                data = json.loads(row["details"])
                lat = data.get("latency", 0)
                hops = data.get("proxy_hops", 0)
                p_size = data.get("payload_size", 0)
            except Exception:
                # If 'details' contains plain text instead of JSON, length & character hash provide basic non-random features
                lat = len(str(row["details"])) * 5
                hops = 1
                p_size = len(str(row["details"]))
        return pd.Series([lat, hops, p_size])

    df[["Latency (ms)", "Proxy Hops", "Payload Size (KB)"]] = df.apply(extract_metrics, axis=1)
    df["Session_ID"] = df["Session_ID"].apply(lambda x: f"SESS_{int(x):04d}")
    return df

df_raw = fetch_telemetry_data()

# Refresh Control
if st.sidebar.button("🔄 Refresh Telemetry"):
    st.rerun()

# Sidebar Controls
st.sidebar.header("⚙️ Anomaly Model Controls")
contamination = st.sidebar.slider("Isolation Forest Contamination", 0.01, 0.20, 0.05, step=0.01)
dbscan_eps = st.sidebar.slider("DBSCAN Epsilon (eps)", 0.1, 2.0, 0.5, step=0.1)
dbscan_min_samples = st.sidebar.slider("DBSCAN Min Samples", 2, 10, 5)

if not df_raw.empty:
    feature_cols = ["Latency (ms)", "Proxy Hops", "Payload Size (KB)"]
    
    iso = IsolationForest(contamination=contamination, random_state=42)
    df_raw["Is_Outlier"] = iso.fit_predict(df_raw[feature_cols])

    scaler = StandardScaler()
    scaled_vals = scaler.fit_transform(df_raw[feature_cols])
    db = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples)
    df_raw["Group_Cluster"] = db.fit_predict(scaled_vals)

    df_raw["Threat Type"] = "✅ Normal Traffic"
    df_raw.loc[df_raw["Is_Outlier"] == -1, "Threat Type"] = "🚨 Lone Outlier"
    df_raw.loc[df_raw["Group_Cluster"] >= 0, "Threat Type"] = "🤖 Coordinated Botnet"

    flagged_threats = df_raw[df_raw["Threat Type"] != "✅ Normal Traffic"]
    total_threats = len(flagged_threats)
    botnet_count = len(df_raw[df_raw["Group_Cluster"] >= 0]["Group_Cluster"].unique())

    # Layout Rendering
    st.markdown("### 🚦 Overall Security Posture")
    col_gauge, col_stats = st.columns([1, 2])

    with col_gauge:
        threat_level = min(100, int((total_threats / max(len(df_raw), 1)) * 100))
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
            st.success("✅ **SYSTEM HEALTHY:** DB logs show operational baseline across active nodes.")
        else:
            st.error("⚠️ **ATTENTION REQUIRED:** System detected operational anomalies in DB logs.")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Database Sessions", len(df_raw))
        m2.metric("Flagged Threats", total_threats, delta=f"{total_threats} alerts", delta_color="inverse")
        m3.metric("Botnet Clusters", botnet_count)

    st.divider()

    st.markdown("### 🎯 Database Log Threats & Mitigation")
    fig_simple = px.scatter(
        df_raw,
        x="Latency (ms)",
        y="Payload Size (KB)",
        color="Threat Type",
        hover_data=["Session_ID", "Proxy Hops"],
        title="DB Telemetry Threat Distribution",
        color_discrete_map={
            "✅ Normal Traffic": "#10B981",
            "🚨 Lone Outlier": "#F59E0B",
            "🤖 Coordinated Botnet": "#EF4444"
        }
    )
    st.plotly_chart(fig_simple, use_container_width=True)

    st.write("#### Flagged Database Logs")
    display_df = flagged_threats[["Session_ID", "Threat Type", "Latency (ms)", "Proxy Hops", "Payload Size (KB)"]]

    if not display_df.empty:
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.markdown("#### ⚡ Automated Action Response")
        col_act1, col_act2 = st.columns([2, 1])

        with col_act1:
            selected_session = st.selectbox("Select Session to Contain:", display_df["Session_ID"].unique())

        with col_act2:
            st.write(" ")
            st.write(" ")
            if st.button("🔒 Isolate & Block Session", type="primary"):
                block_session_in_db(selected_session)
                st.toast(f"✅ Session {selected_session} blocked in database!", icon="🛡️")
                st.rerun()
    else:
        st.info("No active threats detected in database logs.")
else:
    st.info("No unblocked records were returned from the existing `threats_log` table.")