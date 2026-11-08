import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np
from datetime import datetime
from data_engine import generate_mock_data, train_predictive_model

st.set_page_config(page_title="Hyperlocal Q-Commerce Optimizer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-title { font-size:34px !important; font-weight: bold; color: #FF4B4B; text-align: center; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .sub-title { font-size:16px; color: #B0B3B8; text-align: center; margin-bottom: 25px; }
    .metric-card { background-color: #1E1E24; padding: 18px; border-radius: 12px; box-shadow: 3px 5px 12px rgba(0,0,0,0.4); text-align: center; border: 1px solid #3A3B3C; }
    .metric-val { font-size: 28px; font-weight: bold; color: #00E676; margin-top: 5px; }
    .role-badge { background-color: #FF4B4B; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_system():
    df = generate_mock_data()
    models = train_predictive_model(df)
    return models

models = load_system()

# 🔐 ১. এডমিন ও ইউজার প্যানেল সুইচিং সিস্টেম (সাইডবার)
st.sidebar.header("🔐 User Access Management")
user_role = st.sidebar.selectbox("Select Access Control Level", ["👑 Super Admin Control", "🏢 Area Manager Portal", "📊 Sales & Demand Analyst", "🚴 Rider Fulfillment App"])

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Hyperlocal Command Center")
location = st.sidebar.selectbox("📍 Target Operational Hub", ["Dhanmondi Hub (Dhaka)", "Uttara Hub (Dhaka)", "Gulshan Hub (Dhaka)"])

st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Telemetry & Event Overrides")
override_rain = st.sidebar.toggle("🌧️ Sudden Flash Rain Torrent")
override_match = st.sidebar.toggle("🏆 Live Cricket Match (BD vs IND)")
override_night = st.sidebar.toggle("🌙 Late Night Vibe (12 AM - 3 AM)")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Live Micro-Market Drivers")
sim_temp = st.sidebar.slider("Ambient Temperature (°C)", 15, 42, 34 if not override_rain else 22)
sim_rain = st.sidebar.slider("Rain Probability (%)", 0, 100, 95 if override_rain else 15)
sim_social = st.sidebar.slider("Social Buzz Momentum Score", 0, 100, 98 if override_match else 40)

if override_rain: sim_rain = 95
if override_match: sim_social = 98

# ২. প্রেডিক্টিভ ডাটা ক্যালকুলেশন ইঞ্জিন
predictions = {}
for cat, model in models.items():
    pred_input = pd.DataFrame([[sim_temp, sim_rain, sim_social]], columns=['Temperature', 'Rain_Probability', 'Social_Hype'])
    pred_sales = model.predict(pred_input)
    try:
        val = float(np.asarray(pred_sales).flatten())
    except:
        val = 30.0
    if override_rain and cat == 'Rainy Day Comfort (Khichuri/Tea)': val *= 2.5
    if override_match and cat == 'Match Day Snacks (Chips/Popcorn)': val *= 2.8
    if override_night and cat == 'Summer Chill (Ice Cream/Cold Drinks)': val *= 2.0
    live_jitter = np.random.randint(-4, 5)
    predictions[cat] = max(10, int(val + live_jitter))

prices = {'Rainy Day Comfort (Khichuri/Tea)': 120, 'Summer Chill (Ice Cream/Cold Drinks)': 80, 'Match Day Snacks (Chips/Popcorn)': 60, 'Daily Groceries': 250}
margins = {'Rainy Day Comfort (Khichuri/Tea)': 0.35, 'Summer Chill (Ice Cream/Cold Drinks)': 0.40, 'Match Day Snacks (Chips/Popcorn)': 0.45, 'Daily Groceries': 0.20}

total_revenue = 0
total_profit = 0
for cat, units in predictions.items():
    total_revenue += units * prices[cat]
    total_profit += units * prices[cat] * margins[cat]

current_time = datetime.now().strftime("%I:%M:%S %p")

# 🖥️ ৩. ডাইনামিক রোল-বেসড ইন্টারফেস রেন্ডারিং
st.markdown(f'<p class="main-title">⚡ HYPERLOCAL QUICK-COMMERCE ENTERPRISE PLATFORM</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Active Security Context: <span class="role-badge">{user_role}</span> | Node Refreshed: {current_time}</p>', unsafe_allow_html=True)

# ----------------- 👑 SUPER ADMIN CONTROL PANEL -----------------
if user_role == "👑 Super Admin Control":
    st.markdown("### 🎚️ Global System Telemetry (Full Control View)")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">👥 Network Retailers</p><p class="metric-val" style="color:#FFF;">1,248</p><p style="color:#00E676;font-size:11px;margin:0;">↑ 12% System Health</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🟢 Active Stores</p><p class="metric-val" style="color:#00E676;">1,037</p><p style="color:#B0B3B8;font-size:11px;margin:0;">83% Operational Matrix</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📦 Live System Orders</p><p class="metric-val" style="color:#FFBB33;">{sum(predictions.values()) * 3}</p><p style="color:#00E676;font-size:11px;margin:0;">Processing across Dhaka</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">💼 Total Gross Revenue</p><p class="metric-val" style="color:#00E676;">৳ {total_revenue * 3:,}</p><p style="color:#B0B3B8;font-size:11px;margin:0;">All micro-hubs combined</p></div>', unsafe_allow_html=True)
    
    st.info("🛰️ Admin Note: System is sync-monitoring telemetry nodes from all zones. Manual live override overrides automated optimization algorithms.")

# ----------------- 🏢 AREA MANAGER PORTAL -----------------
elif user_role == "🏢 Area Manager Portal":
    st.markdown(f"### 🏙️ Regional Hub Operational Cockpit: {location}")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📍 Local Micro-Market</p><p class="metric-val" style="color:#FFF;font-size:20px;">{location.split()[0]}</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Operational Hub Context</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📊 Optimized Shelf Capacity</p><p class="metric-val" style="color:#00E676;">88.4%</p><p style="color:#B0B3B8;font-size:11px;margin:0;">500 Unit Max Threshold</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🚴 Idle Riders on Bench</p><p class="metric-val" style="color:#FFBB33;">18 Riders</p><p style="color:#FF4B4B;font-size:11px;margin:0;">Avg. Dispatch Time: 9.4 mins</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🚨 Local Stock Risks</p><p class="metric-val" style="color:#FF4B4B;">{"HIGH RISK" if (override_rain or override_match) else "ZERO"}</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Real-time automated alerts</p></div>', unsafe_allow_html=True)

# ----------------- 📊 SALES & DEMAND ANALYST -----------------
elif user_role == "📊 Sales & Demand Analyst":
    st.markdown("### 📈 Machine Learning Demand Prediction Models & Ledger")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🔮 Predicted Next-Hour Units</p><p class="metric-val" style="color:#00E676;">{sum(predictions.values())} Units</p><p style="color:#B0B3B8;font-size:11px;margin:0;">AI Confidence Matrix: 94.6%</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">💰 Projected Gross Revenue</p><p class="metric-val">৳ {total_revenue:,}</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Based on local predictive demand</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📈 Projected Net Margin</p><p class="metric-val" style="color:#00E676;">৳ {int(total_profit):,}</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Dynamic calculation engine</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🧬 Active ML Model</p><p class="metric-val" style="color:#FF4B4B;font-size:18px;">Random Forest Regressor</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Feature-set: Weather+Social</p></div>', unsafe_allow_html=True)

# ----------------- 🚴 RIDER FULFILLMENT APP -----------------
elif user_role == "🚴 Rider Fulfillment App":
    st.markdown("### 🏍️ Live Rider Fulfillment & Last-Mile Dispatch Dashboard")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📦 Orders Ready to Pick</p><p class="metric-val" style="color:#FFBB33;">14 Orders</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Fulfillment SLA target: 15 mins</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🚴 Active Riders in Field</p><p class="metric-val">42 Riders</p><p style="color:#00E676;font-size:11px;margin:0;">Live tracking via geo-nodes</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🌧️ Severe Weather Delay</p><p class="metric-val" style="color:#FF4B4B;">{"+12 Mins" if override_rain else "0 Mins"}</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Dynamic adjustment buffer</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📍 Nearby Cluster Node</p><p class="metric-val" style="color:#FFF;font-size:22px;">Zone Alpha</p><p style="color:#B0B3B8;font-size:11px;margin:0;">Hyperlocal radius 2.5 KM</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ৪. অ্যালার্ট নোটিফিকেশন ইঞ্জিন

