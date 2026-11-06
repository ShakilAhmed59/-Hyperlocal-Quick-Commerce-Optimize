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
    .main-title { font-size:36px !important; font-weight: bold; color: #FF4B4B; text-align: center; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .sub-title { font-size:18px; color: #B0B3B8; text-align: center; margin-bottom: 30px; }
    .metric-card { background-color: #1E1E24; padding: 22px; border-radius: 15px; box-shadow: 3px 5px 15px rgba(0,0,0,0.4); text-align: center; border: 1px solid #3A3B3C; transition: transform 0.2s; }
    .metric-card:hover { transform: scale(1.03); border-color: #FF4B4B; }
    .metric-val { font-size: 32px; font-weight: bold; color: #00E676; margin-top: 5px; }
    .live-pulse { display: inline-block; width: 12px; height: 12px; background: #FF4B4B; border-radius: 50%; box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); animation: pulse 1.2s infinite; vertical-align: middle; margin-right: 8px; }
    @keyframes pulse { 0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); } 70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); } 100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); } }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚡ HYPERLOCAL QUICK-COMMERCE DEMAND OPTIMIZER</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title"><span class="live-pulse"></span>Autonomous Micro-Market Simulation Engine (Streaming Live Data Telemetry)</p>', unsafe_allow_html=True)

@st.cache_data
def load_system():
    df = generate_mock_data()
    models = train_predictive_model(df)
    return models

models = load_system()

st.sidebar.header("🎛️ AI Operations Command Center")
location = st.sidebar.selectbox("📍 Target Dark Store Hub", ["Dhanmondi Hub (Dhaka)", "Uttara Hub (Dhaka)", "Gulshan Hub (Dhaka)"])

st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Manual Vibe & Event Overrides")
override_rain = st.sidebar.toggle("🌧️ Sudden Flash Rain Torrent")
override_match = st.sidebar.toggle("🏆 Live Cricket Match (BD vs IND)")
override_night = st.sidebar.toggle("🌙 Late Night Vibe (12 AM - 3 AM)")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Dynamic Environmental Modifiers")
sim_temp = st.sidebar.slider("Ambient Temperature (°C)", 15, 42, 34 if not override_rain else 22)
sim_rain = st.sidebar.slider("Base Rain Probability (%)", 0, 100, 95 if override_rain else 15)
sim_social = st.sidebar.slider("Socio-Media Momentum Score", 0, 100, 98 if override_match else 40)

if override_rain: sim_rain = 95
if override_match: sim_social = 98

predictions = {}
for cat, model in models.items():
    pred_input = pd.DataFrame([[sim_temp, sim_rain, sim_social]], columns=['Temperature', 'Rain_Probability', 'Social_Hype'])
    pred_sales = model.predict(pred_input)
    
    if override_rain and cat == 'Rainy Day Comfort (Khichuri/Tea)': pred_sales *= 2.5
    if override_match and cat == 'Match Day Snacks (Chips/Popcorn)': pred_sales *= 2.8
    if override_night and cat == 'Summer Chill (Ice Cream/Cold Drinks)': pred_sales *= 2.0
        
    live_jitter = np.random.randint(-4, 5)
predictions[cat] = max(10, int(pred_sales + live_jitter))


prices = {'Rainy Day Comfort (Khichuri/Tea)': 120, 'Summer Chill (Ice Cream/Cold Drinks)': 80, 'Match Day Snacks (Chips/Popcorn)': 60, 'Daily Groceries': 250}
margins = {'Rainy Day Comfort (Khichuri/Tea)': 0.35, 'Summer Chill (Ice Cream/Cold Drinks)': 0.40, 'Match Day Snacks (Chips/Popcorn)': 0.45, 'Daily Groceries': 0.20}

total_revenue = 0
total_profit = 0
for cat, units in predictions.items():
    total_revenue += units * prices[cat]
    total_profit += units * prices[cat] * margins[cat]

current_time = datetime.now().strftime("%I:%M:%S %p")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;font-size:14px;">📡 Live Telemetry Feed</p><p class="metric-val" style="color:#FF4B4B;font-size:24px;">⏱️ {current_time}</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;font-size:14px;">💰 Hourly Gross Revenue</p><p class="metric-val">৳ {total_revenue:,}</p></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;font-size:14px;">📈 Optimized Profit Margin</p><p class="metric-val" style="color:#00E676;">৳ {int(total_profit):,}</p></div>', unsafe_allow_html=True)
with m4:
    dispatch_load = "🚨 CRITICAL" if (override_rain or override_match) else "✅ STABLE"
    color_load = "#FF4B4B" if dispatch_load == "🚨 CRITICAL" else "#00E676"
    st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;font-size:14px;">🚴 Fleet Dispatch Status</p><p class="metric-val" style="color:{color_load};font-size:26px;">{dispatch_load}</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if override_rain:
    st.error(f"🌧️ **CRITICAL ANOMALY DETECTED:** Flash flood conditions active in {location}! Automatically reallocating warehouse capacity to high-priority emergency grocery goods. Rerouting dispatch fleets.")
elif override_match:
    st.success(f"🏆 **HIGH EVENT SURGE:** Localized cricket match momentum spike! Predictive AI has pushed maximum fast-moving snack variants to front-line warehouse pick-bins.")
elif override_night:
    st.warning(f"🌙 **LATE-NIGHT IMPULSE WAVE:** High social media munchies sentiment active. Recommending deep-freeze optimization for cold dessert categories.")
else:
    st.info("🛰️ Autonomous Supply Chain Engine is running optimal configurations. Listening to localized telemetry nodes.")

st.markdown("---")

# 📍 ম্যাপ উইজেট লেআউট
st.subheader(f"🌐 Hyperlocal Geo-Spatial Location: {location}")
geo_data = {
    "Dhanmondi Hub (Dhaka)": {"lat": 23.7461, "lon": 90.3742, "name": "Dhanmondi Dark Store Node A"},
    "Uttara Hub (Dhaka)": {"lat": 23.8759, "lon": 90.3795, "name": "Uttara Dark Store Node B"},
    "Gulshan Hub (Dhaka)": {"lat": 23.7925, "lon": 90.4078, "name": "Gulshan Dark Store Node C"}
}
current_geo = geo_data[location]
map_df = pd.DataFrame([{"lat": current_geo["lat"], "lon": current_geo["lon"], "Store": current_geo["name"]}])
st.map(map_df, zoom=14, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
pred_df = pd.DataFrame(list(predictions.items()), columns=['Category', 'Recommended Stock (Units)'])
total_capacity = 500
pred_df['Shelf Allocation %'] = ((pred_df['Recommended Stock (Units)'] / total_capacity) * 100).round(1)

with col1:
    fig = px.bar(pred_df, x='Category', y='Recommended Stock (Units)', color='Category', 
                 text='Recommended Stock (Units)', title="📊 Real-Time Dynamic Shelf Allocation Framework",
                 color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(template="plotly_dark", showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig_pie = px.pie(pred_df, values='Shelf Allocation %', names='Category', 
                     title="📦 Automated Volumetric Warehouse Space Optimization",
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
    fig_pie.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.subheader("📋 Autonomous Inventory Procurement Ledger")
st.dataframe(pred_df, use_container_width=True)

time.sleep(2)
st.rerun()


