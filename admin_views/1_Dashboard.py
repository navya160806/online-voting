import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# -------------------------------------------------------------------
# 1. PAGE CONFIGURATION & DARK THEME CSS
# -------------------------------------------------------------------
st.set_page_config(page_title="Election Command Center", page_icon="⚡", layout="wide")

DB_NAME = "election_data.db"  # Connected to provided SQLite database

st.markdown("""
<style>
    .glass-card {
        background-color: #121829;
        border: 1px solid #1F293D;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .clock-title { font-size: 0.85rem; color: #8B949E; text-transform: uppercase; letter-spacing: 1px; }
    .clock-time { font-size: 2.1rem; font-weight: 800; color: #00E5FF; font-family: monospace; }
    .clock-date { font-size: 0.9rem; color: #A3B1C6; font-weight: 600; }
    .status-pill { background-color: rgba(0, 229, 255, 0.15); color: #00E5FF; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; border: 1px solid #00E5FF; }
    .party-title { font-size: 1rem; font-weight: 700; color: #FFF; }
    .party-votes { font-size: 1.7rem; font-weight: 800; color: #58A6FF; margin: 2px 0; }
    .party-sub { font-size: 0.8rem; color: #8B949E; }
    .badge-live { background-color: #FF0055; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700;}
    .badge-upcoming { background-color: #FFB703; color: black; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700;}
    .badge-done { background-color: #00F5D4; color: black; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

st.title("⚡ Election Command Center & Live Dashboard")

# Safe SQL Query Helper
def run_query(query, params=()):
    if not os.path.exists(DB_NAME):
        st.error(f"Database file '{DB_NAME}' not found.")
        return pd.DataFrame()
    try:
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.warning(f"Database Query Warning: {e}")
        return pd.DataFrame()

# -------------------------------------------------------------------
# 2. DYNAMIC LIVE FRAGMENT (Auto-refresh every 5 seconds)
# -------------------------------------------------------------------
@st.fragment(run_every="5s")
def render_live_telemetry():
    now = datetime.now()
    current_time_str = now.strftime("%H:%M:%S")
    current_date_str = now.strftime("%A, %b %d, %Y")

    # Fetch System Stats from SQLite
    stats_df = run_query("SELECT active_voters, active_stations, defcon_level FROM system_stats LIMIT 1")
    if not stats_df.empty:
        active_voters = stats_df['active_voters'].iloc[0]
        active_stations = stats_df['active_stations'].iloc[0]
        defcon_level = stats_df['defcon_level'].iloc[0]
    else:
        active_voters, active_stations, defcon_level = 0, "0 / 0", "DEFCON 5"

    # ROW 1: Telemetry Cards
    c1, c2, c3, c4 = st.columns([1.3, 1, 1, 1])

    with c1:
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="clock-title">🌐 Live System Telemetry</span>
                <span class="status-pill">● CONNECTED</span>
            </div>
            <div class="clock-time">{current_time_str}</div>
            <div class="clock-date">{current_date_str}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="glass-card">
            <span class="clock-title">Total Active Voters</span>
            <div class="party-votes" style="color: #00F5D4;">{active_voters:,}</div>
            <div class="party-sub">🟢 Live System DB</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="glass-card">
            <span class="clock-title">Active Polling Stations</span>
            <div class="party-votes" style="color: #7B2CBF;">{active_stations}</div>
            <div class="party-sub">🟢 Station Nodes</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="glass-card">
            <span class="clock-title">Security Status</span>
            <div class="party-votes" style="color: #FFB703;">{defcon_level}</div>
            <div class="party-sub">🟡 System Security</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ROW 2: Political Party Standings
    st.subheader(" Political Party Vote Standings")
    parties_df = run_query("SELECT name, badge, bg, votes, share, color FROM party_standings ORDER BY votes DESC")

    if not parties_df.empty:
        cols = st.columns(len(parties_df))
        for idx, row in parties_df.iterrows():
            with cols[idx]:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="party-title">{row['name']}</span>
                        <span style="background-color: {row['bg']}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: bold;">{row['badge']}</span>
                    </div>
                    <div class="party-votes">{row['votes']:,}</div>
                    <div class="party-sub">Share: <b>{row['share']}%</b></div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No party standings data found.")

    st.markdown("---")

    # ROW 3: State Schedule Cards
    st.subheader(" Election Phases & State Schedule")
    schedules_df = run_query("SELECT state, phase, date, status, badge_class, turnout FROM state_schedules")

    if not schedules_df.empty:
        state_cols = st.columns(len(schedules_df))
        for idx, item in schedules_df.iterrows():
            with state_cols[idx]:
                st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <b style="color: #FFF; font-size: 1rem;">{item['state']}</b>
                        <span class="{item['badge_class']}">{item['status']}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #8B949E;">📅 <b>Date:</b> {item['date']}</div>
                    <div style="font-size: 0.85rem; color: #8B949E;">🏷️ <b>Stage:</b> {item['phase']}</div>
                    <div style="font-size: 0.85rem; color: #58A6FF; margin-top: 4px;">📊 <b>Est. Turnout:</b> {item['turnout']}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No state schedule data found.")

    st.markdown("---")

    # ROW 4: Regional Map & Donut Chart
    m_col1, m_col2 = st.columns([1.5, 1])

    with m_col1:
        st.subheader(" Regional Telemetry & Node Map")
        hubs_df = run_query("SELECT city, lat, lon, voter_density FROM telemetry_hubs")
        if not hubs_df.empty:
            fig_map = px.scatter_mapbox(
                hubs_df, lat="lat", lon="lon", hover_name="city",
                size="voter_density", color="voter_density",
                color_continuous_scale="Electric", size_max=22, zoom=3.8,
                center={"lat": 22.5937, "lon": 78.9629},
                mapbox_style="carto-darkmatter", height=320
            )
            fig_map.update_layout(margin={"r":0, "t":0, "l":0, "b":0}, paper_bgcolor="#121829")
            st.plotly_chart(fig_map, use_container_width=True)

    with m_col2:
        st.subheader("Overall Party Vote Share")
        if not parties_df.empty:
            fig_donut = go.Figure(data=[go.Pie(
                labels=parties_df['name'],
                values=parties_df['votes'],
                hole=.65,
                marker_colors=parties_df['color'].tolist(),
                textinfo='percent'
            )])
            fig_donut.update_layout(
                template="plotly_dark", height=320,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#121829",
                legend=dict(orientation="h", yanchor="top", y=-0.05)
            )
            st.plotly_chart(fig_donut, use_container_width=True)

# Run Live Telemetry Block
render_live_telemetry()