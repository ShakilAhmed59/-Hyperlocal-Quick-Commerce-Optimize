import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np
from datetime import datetime
from data_engine import generate_mock_data, train_predictive_model

st.set_page_config(page_title="Hyperlocal Q-Commerce Enterprise Optimizer", layout="wide", initial_sidebar_state="expanded")

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

st.sidebar.header("🔒 Secure Gateway")
auth_role = st.sidebar.selectbox("Select Your Role:", ["Admin", "Area Manager", "Sales Manager", "Rider"])
auth_email = st.sidebar.text_input("Enter Registered Email", value="shakilshanto899@gmail.com")
auth_phone = st.sidebar.text_input("Enter Phone Number", value="01715233659")
auth_code = st.sidebar.text_input("Enter Unique Auth Code", value="Shakil1024@", type="password")
login_btn = st.sidebar.button("Login to System")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if login_btn:
    if auth_code == "Shakil1024@":
        st.session_state["logged_in"] = True
        st.sidebar.success("🔑 Authentication Successful!")
    else:
        st.session_state["logged_in"] = False
        st.sidebar.error("❌ Invalid Unique Authentication Code!")

if not st.session_state["logged_in"]:
    st.markdown('<p class="main-title">🔒 Hyperlocal Quick-Commerce Enterprise Platform</p>', unsafe_allow_html=True)
    st.warning("⚠️ Access Restricted. Select your designated role and enter valid credentials to unlock the dashboard system.")
    if st.button("Unlock Demo View for Presentation"):
        st.session_state["logged_in"] = True
        st.rerun()
    st.stop()

st.sidebar.markdown("---")
st.sidebar.header("🎛️ AI Command Center")
location = st.sidebar.selectbox("📍 Target Operational Hub", ["Dhanmondi Hub (Dhaka)", "Uttara Hub (Dhaka)", "Gulshan Hub (Dhaka)"])

st.sidebar.markdown("---")
st.sidebar.subheader("🕹️ Telemetry Event Overrides")
override_rain = st.sidebar.toggle("🌧️ Sudden Flash Rain Torrent")
override_match = st.sidebar.toggle("🏆 Live Cricket Match (BD vs IND)")
override_night = st.sidebar.toggle("🌙 Late Night Vibe (12 AM - 3 AM)")

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Live Drivers")
sim_temp = st.sidebar.slider("Ambient Temperature (°C)", 15, 42, 34 if not override_rain else 22)
sim_rain = st.sidebar.slider("Base Rain Probability (%)", 0, 100, 95 if override_rain else 15)
sim_social = st.sidebar.slider("Social Buzz Score", 0, 100, 98 if override_match else 40)

if override_rain: sim_rain = 95
if override_match: sim_social = 98

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

st.markdown(f'<p class="main-title">⚡ HYPERLOCAL QUICK-COMMERCE ENTERPRISE PLATFORM</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title"> Active Secure Role: <span class="role-badge">{auth_role}</span> | Telemetry Sync: {current_time}</p>', unsafe_allow_html=True)

if auth_role == "Admin":
    st.markdown("###  Global System Telemetry (Admin Full Control)")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">👥 Total Retailers</p><p class="metric-val" style="color:#FFF;">1,248</p><p style="color:#00E676;font-size:11px;margin:0;">↑ 12% +86 this month</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🟢 Active Network</p><p class="metric-val" style="color:#00E676;">1,037</p><p style="color:#B0B3B8;font-size:11px;margin:0;">83% Operational Capacity</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📦 Supply-Demand Alerts</p><p class="metric-val" style="color:#FFBB33;">17 Alerts</p><p style="color:#FF4B4B;font-size:11px;margin:0;">Active discrepancies flagged</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">💼 Global Revenue</p><p class="metric-val" style="color:#00E676;">৳ {total_revenue * 3:,}</p><p style="color:#B0B3B8;font-size:11px;margin:0;">All target nodes aggregated</p></div>', unsafe_allow_html=True)

elif auth_role == "Area Manager":
    st.markdown(f"###  Regional Hub Cockpit: {location}")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📍 Operational Zone</p><p class="metric-val" style="color:#FFF;font-size:20px;">{location}</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;"> Active Demand Areas</p><p class="metric-val" style="color:#00E676;">11 Districts</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">🚴 Dispatch Fleet Idle</p><p class="metric-val" style="color:#FFBB33;">18 Riders</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">⚠️ Risk Level Score</p><p class="metric-val" style="color:#FF4B4B;">{"CRITICAL" if override_rain else "STABLE"}</p></div>', unsafe_allow_html=True)

else:
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">💰 Projected Revenue</p><p class="metric-val">৳ {total_revenue:,}</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📈 Profit Optimization</p><p class="metric-val" style="color:#00E676;">৳ {int(total_profit):,}</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">⏱️ Execution SLA</p><p class="metric-val" style="color:#FFBB33;">15 Mins Target</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p style="color:#B0B3B8;margin:0;">📡 Pipeline Status</p><p class="metric-val" style="color:#00E676;">Connected & Online</p></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if override_rain: st.error(f"🌧️ **CRITICAL ANOMALY DETECTED:** Flash flood conditions active in {location}! Reallocating warehouse capacity to emergency grocery goods.")
elif override_match: st.success(f"🏆 **HIGH EVENT SURGE:** Localized cricket match momentum spike! Predictive AI variants pushed to front-line warehouse pick-bins.")
elif override_night: st.warning(f"🌙 **LATE-NIGHT IMPULSE WAVE:** High social media munchies sentiment active. Recommending optimization for cold dessert categories.")
else: st.info("🛰️ Supply chain telemetry data pipeline is clear. Processing automated localized configurations.")

st.markdown("---")

st.subheader(" Live Emergency Demand & Micro-Market Geospatial Map")
area_locations = {
    'Ashulia': [23.8931, 90.3235], 'DIU Campus': [23.8768, 90.3201], 'Dhamrai': [23.9189, 90.2163],
    'Eastern University': [23.9300, 90.2800], 'Mirpur 1': [23.7956, 90.3537], 'Mirpur 10': [23.8069, 90.3687],
    'Mirpur 2': [23.8011, 90.3600], 'Nobinagar': [23.9133, 90.2678], 'Pollibiddut': [23.9055, 90.2788],
    'Savar': [23.8583, 90.2667], 'Uttara': [23.8759, 90.3795]
}
map_list = []
for area, coords in area_locations.items():
    map_list.append({"lat": coords[0], "lon": coords[1], "Area": area})
st.map(pd.DataFrame(map_list), zoom=10, use_container_width=True)

st.markdown("---")

col_t1, col_t2 = st.columns(2)

with col_t1:
    st.subheader(" Area-wise Demand Density")
    density_df = pd.DataFrame({
        'area': ['Ashulia', 'DIU Campus', 'Dhamrai', 'Eastern Univ', 'Mirpur 1', 'Mirpur 10', 'Mirpur 2', 'Nobinagar', 'Pollibiddut', 'Savar'],
        'total_requests':,
        'category_breakdown': ['{"Food":1}', '{"Medicine":1}', '{"Medicine":1}', '{"Emergency":1}', '{"Medicine":1}', '{"Medicine":1}', '{"Medicine":1}', '{"Medicine":1}', '{"Medicine":1}', '{"Water":1}'],
        'priority': ['High', 'Critical', 'Medium', 'High', 'Low', 'Critical', 'Medium', 'High', 'Low', 'Medium']
    })
