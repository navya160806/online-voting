import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# -------------------------------------------------------------------
# 1. PAGE CONFIGURATION & DARK THEME CSS
# -------------------------------------------------------------------
st.title("⚡ Election Command Center & Live Dashboard")

st.markdown("""
<style>
    /* Sleek Rounded Cards */
    .glass-card {
        background-color: #121829;
        border: 1px solid #1F293D;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .clock-title {
        font-size: 0.85rem;
        color: #8B949E;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .clock-time {
        font-size: 2.1rem;
        font-weight: 800;
        color: #00E5FF;
        font-family: monospace;
    }
    
    .clock-date {
        font-size: 0.9rem;
        color: #A3B1C6;
        font-weight: 600;
    }
    
    .status-pill {
        background-color: rgba(0, 229, 255, 0.15);
        color: #00E5FF;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        border: 1px solid #00E5FF;
    }

    /* Party Cards */
    .party-title { font-size: 1rem; font-weight: 700; color: #FFF; }
    .party-votes { font-size: 1.7rem; font-weight: 800; color: #58A6FF; margin: 2px 0; }
    .party-sub { font-size: 0.8rem; color: #8B949E; }
    
    /* State Schedule Badges */
    .badge-live { background-color: #FF0055; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700;}
    .badge-upcoming { background-color: #FFB703; color: black; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700;}
    .badge-done { background-color: #00F5D4; color: black; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: 700;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 2. ROW 1: LIVE TIME, SYSTEM CLOCK & QUICK STATS
# -------------------------------------------------------------------
now = datetime.now()
current_time_str = now.strftime("%H:%M:%S")
current_date_str = now.strftime("%A, %b %d, %Y")

c1, c2, c3, c4 = st.columns([1.3, 1, 1, 1])

with c1:
    st.markdown(f"""
    <div class="glass-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="clock-title">🌐 Live System Telemetry</span>
            <span class="status-pill">● SYNCED (IST)</span>
        </div>
        <div class="clock-time">{current_time_str}</div>
        <div class="clock-date">{current_date_str}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card">
        <span class="clock-title">Total Active Voters</span>
        <div class="party-votes" style="color: #00F5D4;">124,850</div>
        <div class="party-sub">⬆ +12.4% vs Phase 1</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="glass-card">
        <span class="clock-title">Active Polling Stations</span>
        <div class="party-votes" style="color: #7B2CBF;">1,420 / 1,500</div>
        <div class="party-sub">🟢 94.6% Online</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="glass-card">
        <span class="clock-title">Security DEFCON</span>
        <div class="party-votes" style="color: #FFB703;">DEFCON 4</div>
        <div class="party-sub">🟡 Nominal Monitoring</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------------
# 3. ROW 2: THREE POLITICAL PARTIES STANDINGS CARDS
# -------------------------------------------------------------------
st.subheader(" Political Party Vote Standings")

parties_data = [
    {"name": "Progressive Alliance (PA)", "badge": "LEAD", "bg": "#8A2BE2", "votes": 48290, "share": 44.2, "color": "#8A2BE2"},
    {"name": "Democratic Coalition (DC)", "badge": "RUNNER UP", "bg": "#00E5FF", "votes": 39140, "share": 35.8, "color": "#00E5FF"},
    {"name": "National Reform Front (NRF)", "badge": "THIRD", "bg": "#FF007F", "votes": 21820, "share": 20.0, "color": "#FF007F"}
]

p1, p2, p3 = st.columns(3)
cols = [p1, p2, p3]

for i, p in enumerate(parties_data):
    with cols[i]:
        np.random.seed(i + 10)
        spark_y = np.cumsum(np.random.randn(12) + 1) + (p["votes"] * 0.8)
        
        fig_spark = go.Figure(go.Scatter(
            y=spark_y, mode='lines', line=dict(color=p["color"], width=2),
            fill='tozeroy', fillcolor=f"rgba(100, 100, 250, 0.1)"
        ))
        fig_spark.update_layout(height=45, margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(visible=False), yaxis=dict(visible=False), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; justify-content: space-between;">
                <span class="party-title">{p['name']}</span>
                <span style="background-color: {p['bg']}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; font-weight: bold;">{p['badge']}</span>
            </div>
            <div class="party-votes">{p['votes']:,}</div>
            <div class="party-sub">Share: <b>{p['share']}%</b></div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})

st.markdown("---")

# -------------------------------------------------------------------
# 4. ROW 3: STATE ELECTION SCHEDULE & DATES CARDS
# -------------------------------------------------------------------
st.subheader(" Election Phases & State Schedule")

s1, s2, s3, s4 = st.columns(4)

states_schedule = [
    {"state": "Uttar Pradesh", "phase": "Phase 1", "date": "Jul 30, 2026", "status": "LIVE NOW", "badge_class": "badge-live", "turnout": "74.2%"},
    {"state": "Maharashtra", "phase": "Phase 2", "date": "Aug 02, 2026", "status": "UPCOMING", "badge_class": "badge-upcoming", "turnout": "Pending"},
    {"state": "Delhi NCR", "phase": "Phase 1", "date": "Jul 30, 2026", "status": "COMPLETED", "badge_class": "badge-done", "turnout": "81.5%"},
    {"state": "Karnataka", "phase": "Phase 3", "date": "Aug 05, 2026", "status": "UPCOMING", "badge_class": "badge-upcoming", "turnout": "Pending"}
]

state_cols = [s1, s2, s3, s4]

for idx, item in enumerate(states_schedule):
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

st.markdown("---")

# -------------------------------------------------------------------
# 5. ROW 4: INDIA GEOGRAPHIC MAP & VOTE VELOCITY GRAPH
# -------------------------------------------------------------------
m_col1, m_col2 = st.columns([1.5, 1])

with m_col1:
    st.subheader(" India Regional Telemetry & Node Map")
    
    india_hubs = pd.DataFrame({
        'city': ['Lucknow', 'Delhi', 'Mumbai', 'Bengaluru', 'Kolkata', 'Hyderabad', 'Jaipur'],
        'lat': [26.8467, 28.6139, 19.0760, 12.9716, 22.5726, 17.3850, 26.9124],
        'lon': [80.9462, 77.2090, 72.8777, 77.5946, 88.3639, 78.4867, 75.7873],
        'voter_density': [95, 140, 180, 110, 85, 90, 60]
    })

    fig_map = px.scatter_mapbox(
        india_hubs, lat="lat", lon="lon", hover_name="city",
        size="voter_density", color="voter_density",
        color_continuous_scale="Electric", size_max=22, zoom=4.0,
        center={"lat": 22.5937, "lon": 78.9629},
        mapbox_style="carto-darkmatter", height=320
    )
    fig_map.update_layout(margin={"r":0, "t":0, "l":0, "b":0}, paper_bgcolor="#121829")
    st.plotly_chart(fig_map, use_container_width=True)

with m_col2:
    st.subheader("Overall Party Vote Share")
    
    fig_donut = go.Figure(data=[go.Pie(
        labels=[p["name"] for p in parties_data],
        values=[p["votes"] for p in parties_data],
        hole=.65,
        marker_colors=['#8A2BE2', '#00E5FF', '#FF007F'],
        textinfo='percent'
    )])
    
    fig_donut.update_layout(
        template="plotly_dark", height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="#121829",
        legend=dict(orientation="h", yanchor="top", y=-0.05)
    )
    st.plotly_chart(fig_donut, use_container_width=True)