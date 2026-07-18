import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

# --- 1. SECURITY GATING ENGINE ---
if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

# --- 2. VOTE MATRIX & TELEMETRY STATE MANAGER ---
if "party_votes" not in st.session_state:
    st.session_state["party_votes"] = {
        "Cyber Democratic Front (CDF)": 845200,
        "National Tech Vanguard (NTV)": 812450,
        "Libertarian Crypto Union (LCU)": 415300
    }
    st.session_state["threat_count"] = 1253

# Simulate dynamic live updates per cycle
st.session_state["party_votes"]["Cyber Democratic Front (CDF)"] += random.randint(45, 120)
st.session_state["party_votes"]["National Tech Vanguard (NTV)"] += random.randint(40, 130)
st.session_state["party_votes"]["Libertarian Crypto Union (LCU)"] += random.randint(15, 60)
st.session_state["threat_count"] += random.choice([-1, 0, 1, 2])

# Calculate leaderboard sorting metrics
sorted_parties = sorted(st.session_state["party_votes"].items(), key=lambda x: x[1], reverse=True)
leading_party_name, leading_party_votes = sorted_parties[0]
total_votes = sum(st.session_state["party_votes"].values())
lead_margin = leading_party_votes - sorted_parties[1][1]

# Dynamic UI metrics
risk_score = random.randint(78, 83)
network_health = random.randint(97, 99)

# Silent JS clock trigger forces re-execution every 4 seconds without widget artifacts
st.components.v1.html(
    """
    <script>
        window.parent.document.dispatchEvent(new CustomEvent("streamlit:render"));
        setTimeout(function() {
            window.parent.document.querySelector('.stApp').click(); 
        }, 4000);
    </script>
    """,
    height=0,
)

# --- 3. DENSE CYBERPUNK HUD DESIGN STYLE CSS ---
st.markdown("""
    <style>
        /* Global Background Reset */
        .stApp {
            background-color: #0B0F17 !important;
        }
        
        [data-testid="stHeader"], [data-testid="stWidgetFormProps"] {
            background: transparent !important;
        }
        
        /* Unified Modular Matte Control Panels */
        .hud-panel {
            background-color: #111622 !important;
            border: 1px solid #1F293D !important;
            border-radius: 6px;
            padding: 16px;
            margin-bottom: 10px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5);
        }
        
        /* Metric Typography Layouts */
        .hud-label {
            color: #64748B;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 4px;
        }
        
        .hud-value {
            font-family: 'Courier New', monospace;
            font-size: 26px;
            font-weight: 700;
            line-height: 1.1;
        }
        
        .hud-sub {
            font-size: 11px;
            margin-top: 6px;
            font-weight: 500;
        }
        
        /* Leaderboard Specific Elements */
        .party-rank {
            font-size: 10px;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 3px;
            margin-right: 6px;
            vertical-align: middle;
        }
        
        /* Dense Data Tables */
        .cyber-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-top: 8px;
        }
        .cyber-table th {
            color: #475569;
            text-align: left;
            padding: 10px 6px;
            border-bottom: 2px solid #1F293D;
            text-transform: uppercase;
            font-size: 10px;
        }
        .cyber-table td {
            padding: 12px 6px;
            border-bottom: 1px solid #161B26;
            color: #E2E8F0;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. TOP HUD ROW: TITLE HEADLINE ---
st.markdown("<h2 style='color:#FFFFFF; margin:0 0 4px 0; font-size:24px; font-weight:400; letter-spacing:0.5px;'>ENTERPRISE SECURITY <span style='color:#38BDF8; font-size:14px; margin-left:10px; font-weight:700;'>• TACTICAL ELECTION TELEMETRY</span></h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:0; border-top:1px solid #1F293D; margin:10px 0 20px 0;'>", unsafe_allow_html=True)

# --- 5. TOP ROW LAYER: DYNAMIC TOP 3 PARTIES LEADERBOARD CARDS ---
st.markdown("<div style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 1px; margin-bottom: 8px;'>REAL-TIME REGISTRY STANDINGS</div>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)

colors = ["#38BDF8", "#F59E0B", "#A855F7"]
badges = [("🥇 1ST", "#0C4A6E"), ("🥈 2ND", "#78350F"), ("🥉 3RD", "#4C1D95")]

for idx, (name, votes) in enumerate(sorted_parties):
    pct = (votes / total_votes) * 100
    target_col = p_col1 if idx == 0 else (p_col2 if idx == 1 else p_col3)
    
    with target_col:
        st.markdown(f"""
            <div class="hud-panel" style="border-left: 4px solid {colors[idx]} !important;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span class="hud-label" style="color: #E2E8F0; margin: 0; font-size: 12px;">{name}</span>
                    <span class="party-rank" style="background: {badges[idx][1]}; color: {colors[idx]};">{badges[idx][0]}</span>
                </div>
                <div class="hud-value" style="color: #FFFFFF;">{votes:,} <span style="font-size: 14px; color: #64748B; font-weight: normal;">({pct:.2f}%)</span></div>
                <div class="hud-sub" style="color: #64748B;">
                    {"🔥 Current Leader" if idx == 0 else f"▼ Trailing by {leading_party_votes - votes:,} votes"}
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 6. MIDDLE VISUAL DIAGNOSTICS ROW (INCORPORATING LIVE MARGIN GAUGE) ---
mid_left, mid_center, mid_right = st.columns([1.5, 1.2, 2.3])

with mid_left:
    st.markdown('<div class="hud-panel" style="height:270px; text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div class="hud-label" style="text-align:left;">CONSOLIDATED TELEMETRY MARGIN</div>', unsafe_allow_html=True)
    
    # Gauge represents leading share proportion
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=int((leading_party_votes / total_votes) * 100), domain={'x': [0, 1], 'y': [0, 1]},
        number={'font': {'color': '#38BDF8', 'size': 44, 'family': 'Courier New, monospace'}, 'suffix': '%'},
        gauge={
            'axis': {'range': [None, 100], 'visible': False}, 
            'bar': {'color': "#38BDF8", 'thickness': 0.16}, 
            'bgcolor': "#161B26", 
            'steps': [{'range': [0, 100], 'color': '#161B26'}], 
            'borderwidth': 0
        }
    ))
    fig_gauge.update_layout(height=130, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='#111622', plot_bgcolor='#111622')
    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
    
    # Explicit text indicators pointing to the current frontrunner
    st.markdown(f"""
        <div style="margin-top: 2px;">
            <div style="font-size: 11px; color: #64748B; font-weight:700; text-transform: uppercase; letter-spacing:0.5px;">SYSTEM LEADER:</div>
            <div style="color: #38BDF8; font-weight: 700; font-size: 14px; font-family: monospace;">{leading_party_name}</div>
            <div style="color: #10B981; font-size: 11px; font-weight:500; margin-top: 2px;">⚡ Margin Split: +{lead_margin:,} votes</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with mid_center:
    st.markdown('<div class="hud-panel" style="height:270px;">', unsafe_allow_html=True)
    st.markdown('<div class="hud-label">INTEGRITY NODE SCANS</div>', unsafe_allow_html=True)
    
    spark_data = [random.randint(40, 65) for _ in range(15)]
    fig_spark = go.Figure(go.Scatter(y=spark_data, mode='lines', line=dict(color='#10B981', width=2, shape='spline'), fill='tozeroy', fillcolor='rgba(16,185,129,0.06)'))
    fig_spark.update_layout(height=130, margin=dict(l=0, r=0, t=5, b=5), paper_bgcolor='#111622', plot_bgcolor='#111622', xaxis=dict(visible=False), yaxis=dict(visible=False))
    st.plotly_chart(fig_spark, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<div style="background:#161B26; border-radius:4px; padding:10px; margin-top:15px; text-align:center; border:1px solid #1F293D;"><span style="color:#10B981; font-weight:700; font-size:12px; letter-spacing:0.5px;">✓ TELEMETRY PIPELINE SECURE</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with mid_right:
    st.markdown('<div class="hud-panel" style="height:270px;">', unsafe_allow_html=True)
    st.markdown('<div class="hud-label">GLOBAL INGESTION MAP LAYER</div>', unsafe_allow_html=True)
    
    fig_map = go.Figure(go.Scattergeo(lat=[20, 40, -20, 10, 50, -10], lon=[77, -100, -60, 20, 10, 120], marker=dict(size=[14, 18, 12, 22, 15, 16], color='#EF4444', opacity=0.7, line=dict(width=1, color='#FFFFFF'))))
    fig_map.update_layout(geo=dict(scope='world', showland=True, landcolor='#161B26', showcountries=True, countrycolor='#1F293D', showocean=False, bgcolor='rgba(0,0,0,0)', showframe=False), margin=dict(l=0, r=0, t=0, b=0), height=210, paper_bgcolor='#111622')
    st.plotly_chart(fig_map, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. BOTTOM HUD ROW: INFRASTRUCTURE METRICS & THREAT CONTROLS ---
bottom_left, bottom_right = st.columns([1.8, 2.2])

with bottom_left:
    st.markdown('<div class="hud-panel" style="height:280px;">', unsafe_allow_html=True)
    st.markdown('<div class="hud-label">CORE INFRASTRUCTURE NETWORKS</div>', unsafe_allow_html=True)
    
    stat_b1, stat_b2 = st.columns(2)
    with stat_b1:
        st.markdown(f'<div style="background:#161B26; padding:12px; border-radius:4px; border:1px solid #1F293D;"><div class="hud-label">Threat Vector</div><div class="hud-value" style="color:#EF4444; font-size:22px;">{st.session_state["threat_count"]:,}</div><span style="color:#7F1D1D; font-size:10px; font-weight:bold;">Isolations Active</span></div>', unsafe_allow_html=True)
    with stat_b2:
        st.markdown(f'<div style="background:#161B26; padding:12px; border-radius:4px; border:1px solid #1F293D;"><div class="hud-label">Health Index</div><div class="hud-value" style="color:#10B981; font-size:22px;">{network_health}%</div><span style="color:#064E3B; font-size:10px; font-weight:bold;">Optimal Node state</span></div>', unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top:14px;' class='hud-label'>SYSTEM VULNERABILITY STATUS: <span style='color:#38BDF8;'>342 CONTAINERS STABLE</span></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with bottom_right:
    st.markdown('<div class="hud-panel" style="height:280px; overflow:hidden;">', unsafe_allow_html=True)
    st.markdown('<div class="hud-label">CORE ASSET BALANCING LEDGER</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <table class="cyber-table">
            <thead>
                <tr>
                    <th>Asset Identifier</th>
                    <th>Cluster Weight</th>
                    <th>Index Accuracy</th>
                    <th>Operational State</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="font-family:monospace; color:#38BDF8; font-weight:600;">SYS_SERVER_01</td>
                    <td>1,120 req/s</td>
                    <td style="color:#10B981; font-weight:600;">99.84%</td>
                    <td><span style="background:#064E3B; color:#10B981; padding:2px 6px; border-radius:3px; font-size:10px; font-weight:700;">OPTIMAL</span></td>
                </tr>
                <tr>
                    <td style="font-family:monospace; color:#38BDF8; font-weight:600;">SYS_SERVER_02</td>
                    <td>1,480 req/s</td>
                    <td style="color:#10B981; font-weight:600;">99.08%</td>
                    <td><span style="background:#064E3B; color:#10B981; padding:2px 6px; border-radius:3px; font-size:10px; font-weight:700;">OPTIMAL</span></td>
                </tr>
                <tr>
                    <td style="font-family:monospace; color:#38BDF8; font-weight:600;">DB_CLUSTER_EAST</td>
                    <td>{random.randint(800,990)} req/s</td>
                    <td style="color:#F59E0B; font-weight:600;">97.42%</td>
                    <td><span style="background:#78350F; color:#F59E0B; padding:2px 6px; border-radius:3px; font-size:10px; font-weight:700;">WARNING</span></td>
                </tr>
            </tbody>
        </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)