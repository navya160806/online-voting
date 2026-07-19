import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Safety check: Initialize the key if Streamlit pre-runs this file out of order
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 1. SECURITY CHECK: Protect the view from unauthorized direct URL entry
if not st.session_state.get("authenticated", False):
    st.error("🔒 Unauthorized access. Please log in through the main portal.")
    st.stop()

# 2. CUSTOM CSS: Injection for Rounded Cards and Metric Styling
st.markdown("""
    <style>
        /* Modern Card Containers */
        .metric-card {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 22px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.04);
            margin-bottom: 15px;
            border: 1px solid #E2E8F0;
        }
        
        .metric-title {
            color: #718096;
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 2px;
        }
        
        .metric-sub {
            color: #A0AEC0;
            font-size: 12px;
        }
        
        /* Threat Feed Container styling */
        .threat-container {
            height: 290px; 
            overflow-y: auto;
        }
        
        .threat-item {
            border-bottom: 1px solid #EDF2F7; 
            padding-bottom: 10px; 
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. TOP NAVIGATION HEADER BAR (Search & Profile Mock)
head_col1, head_col2 = st.columns([4, 1])
with head_col1:
    st.text_input("🔍 Search system records...", placeholder="Search logs, voter IDs, or network profiles...", label_visibility="collapsed")
with head_col2:
    st.markdown("<p style='text-align: right; color: #4A5568; margin-top: 6px;'>Hi, <b>Chief Auditor</b> 👤</p>", unsafe_allow_html=True)

st.write("---")

# 4. ROW 1: Detailed Main Line Chart (System Performance & Network Influx)
st.markdown("### 📈 Live Election System Performance & Active Nodes")

# Simulating historical voting telemetry load data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
values = [3200, 4100, 1900, 4300, 4900, 5900, 3900, 4800]

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(
    x=months, y=values,
    mode='lines+markers',
    line=dict(color='#F59E0B', width=3), # Warm gold line matching UI
    marker=dict(size=8, color='#3B82F6'),
    name="Traffic Stream"
))

fig_line.update_layout(
    margin=dict(l=20, r=20, t=10, b=10),
    height=280,
    paper_bgcolor='white',
    plot_bgcolor='white',
    xaxis=dict(showgrid=True, gridcolor='#EDF2F7'),
    yaxis=dict(showgrid=True, gridcolor='#EDF2F7')
)
st.plotly_chart(fig_line, use_container_width=True)

st.write("")

# 5. ROW 2: The Three Modern Custom Metrics Cards
card_col1, card_col2, card_col3 = st.columns(3)

with card_col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Voter Ingest Velocity</div>
            <div class="metric-value" style="color: #3B82F6;">$ 2723</div>
            <div class="metric-sub">▲ 12% baseline traffic influx</div>
        </div>
    """, unsafe_allow_html=True)

with card_col2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Total Verified Ballots</div>
            <div class="metric-value" style="color: #F59E0B;">2,142,950</div>
            <div class="metric-sub">98.4% cryptographic validation rate</div>
        </div>
    """, unsafe_allow_html=True)

with card_col3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Resolved Security Alerts</div>
            <div class="metric-value" style="color: #10B981;">232,000</div>
            <div class="metric-sub">✓ 100% of pipeline threats auto-mitigated</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# 6. ROW 3: Encryption Radial Gauge, Regional Bar Chart, & Live Active Threats
bottom_col1, bottom_col2, bottom_col3 = st.columns([1.2, 1.8, 1.5])

# Bottom Card 1: Radial Progress Circle (75%)
with bottom_col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight: 600; color: #4A5568; margin-bottom:0;'>Profile Strength / Encryption Health</p>", unsafe_allow_html=True)
    
    fig_radial = go.Figure(go.Indicator(
        mode="gauge+number",
        value=75,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100], 'visible': False},
            'bar': {'color': "#F59E0B"}, # Accent gauge matching mock-up ring
            'bgcolor': "#EDF2F7",
            'borderwidth': 0
        }
    ))
    fig_radial.update_layout(height=230, margin=dict(l=30, r=30, t=20, b=10))
    st.plotly_chart(fig_radial, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom Card 2: Categorical Bar Chart (Detailed Chart 02)
with bottom_col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("<p style='font-weight: 600; color: #4A5568; margin-bottom:5px;'>Detailed Regional Loads</p>", unsafe_allow_html=True)
    
    regions = ['Reg A', 'Reg B', 'Reg C', 'Reg D', 'Reg E']
    loads = [1200, 4100, 3500, 5300, 6800]
    colors = ['#FF5A5F', '#3B82F6', '#F59E0B', '#10B981', '#8B5CF6']
    
    fig_bar = go.Figure(data=[go.Bar(x=regions, y=loads, marker_color=colors, width=0.4)])
    fig_bar.update_layout(
        height=225,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#E2E8F0')
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Bottom Card 3: Recently News Ledger
with bottom_col3:
    st.markdown("""
        <div class="metric-card threat-container">
            <p style="font-weight: 600; color: #4A5568; margin-bottom: 12px;">Recently Threat Activity</p>
            <div class="threat-item">
                <span style="font-size: 11px; color: #EF4444; font-weight: bold;">05:30 AM</span>
                <p style="font-size: 13px; margin: 0; color: #2D3748;">DBSCAN detected anomalous cluster pattern in Precinct 4</p>
            </div>
            <div class="threat-item">
                <span style="font-size: 11px; color: #3B82F6; font-weight: bold;">04:15 AM</span>
                <p style="font-size: 13px; margin: 0; color: #2D3748;">Routine server configuration backup process finalized</p>
            </div>
            <div class="threat-item" style="border-bottom: none; padding-bottom: 0; margin-bottom: 0;">
                <span style="font-size: 11px; color: #EF4444; font-weight: bold;">02:10 AM</span>
                <p style="font-size: 13px; margin: 0; color: #2D3748;">Isolation forest flagged borderline signature deviation</p>
            </div>
        </div>
    """, unsafe_allow_html=True)