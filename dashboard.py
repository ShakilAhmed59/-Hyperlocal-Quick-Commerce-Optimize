import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import time

st.set_page_config(
    page_title="Hyperlocal Q-Commerce Optimizer",
    page_icon="🚨",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8080"

st.title("🚨 Hyperlocal Q-Commerce & Emergency Supply Dashboard")
st.markdown("Real-time Smart Demand Detection and Core Operations Analytics Panel.")

try:
    response = requests.get(f"{API_BASE_URL}/")
    if response.status_code == 200:
        st.success("⚡ Backend API Server: Connected & Online")
except requests.exceptions.ConnectionError:
    st.error("❌ Backend Server Offline! Please run 'python app.py' in your VS Code terminal first.")
    st.stop()

st.sidebar.header("🕹️ Control Panel")
st.sidebar.info("🔄 Auto-refreshing dashboard data every 3 seconds...")

def fetch_api_data(endpoint):
    try:
        res = requests.get(f"{API_BASE_URL}{endpoint}")
        if res.status_code == 200 and res.json().get("success"):
            return res.json().get("data", [])
    except Exception:
        return []
    return []

demand_summary = fetch_api_data("/api/demand/summary")
emergency_demands = fetch_api_data("/api/demand/emergency")
demand_gap = fetch_api_data("/api/demand/gap")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric(label="Total Active Demand Areas", value=len(demand_summary) if demand_summary else 0)
with m2:
   emergency_demands = fetch_api_data("/api/demand/gap")

with m3:
    st.metric(label="Supply-Demand Gap Alerts", value=len(demand_gap) if demand_gap else 0)

st.markdown("---")

st.subheader("📍 Live Emergency Demand Geospatial Map")
col_map, col_list = st.columns(2)

map_center = [23.8600, 90.3000] 
m = folium.Map(location=map_center, zoom_start=11, tiles="OpenStreetMap")

if emergency_demands:
    for item in emergency_demands:
        lat = item.get("latitude") or item.get("lat")
        lon = item.get("longitude") or item.get("lon")
        category = item.get("category") or "General Supply"
        product_name = item.get("product_name") or "Not Specified"
        qty = item.get("quantity") or item.get("qty") or 0
        area = item.get("area") or "Unknown Area"
        urgency = item.get("urgency") or "High"
        
        if not lat or not lon or lat == 0 or lon == 0:
            area_lower = str(area).lower()
            if "ashulia" in area_lower:
                lat, lon = 23.9000, 90.3300
            elif "dhamrai" in area_lower:
                lat, lon = 23.9167, 90.2167
            elif "savar" in area_lower:
                lat, lon = 23.8583, 90.2667
            elif "nobinagar" in area_lower:
                lat, lon = 23.8920, 90.2642
            elif "pollibiddut" in area_lower or "polli biddut" in area_lower:
                lat, lon = 23.8728, 90.2794
            elif "campus" in area_lower or "diu" in area_lower:
                lat, lon = 23.8766, 90.3204
            elif "eastern" in area_lower or "esturn" in area_lower:
                lat, lon = 23.8794, 90.3235
            elif "uttara" in area_lower:
                lat, lon = 23.8759, 90.3795
            elif "mirpur 10" in area_lower or "mirpur10" in area_lower:
                lat, lon = 23.8069, 90.3688
            elif "mirpur 2" in area_lower or "mirpur2" in area_lower:
                lat, lon = 23.8051, 90.3619
            elif "mirpur 1" in area_lower or "mirpur1" in area_lower:
                lat, lon = 23.7956, 90.3537
            else:
                lat, lon = 23.8600, 90.3000

        color = "red" if str(urgency).lower() in ["critical", "high"] or int(qty) > 20 else "orange"
        
        popup_text = f"""
        <div style="font-family: Arial, sans-serif; width: 180px;">
            <h4 style="margin:0 0 5px 0; color:red;">🚨 Emergency Need</h4>
            <b>Area:</b> {area}<br>
            <b>Type:</b> {category}<br>
            <b>Product:</b> {product_name}<br>
            <b>Quantity:</b> {qty}<br>
        </div>
        """
        folium.Marker(
            location=[float(lat), float(lon)],
            popup=folium.Popup(popup_text, max_width=250),
            tooltip=f"{product_name} in {area}",
            icon=folium.Icon(color=color, icon="exclamation-sign")
        ).add_to(m)

with col_map:
    st_folium(m, width=650, height=450, key="live_map", returned_objects=[])

with col_list:
    st.markdown("### 📋 Active Emergency Product Requests")
    if emergency_demands:
        df_emergency = pd.DataFrame(emergency_demands)
        st.dataframe(df_emergency, use_container_width=True, height=400)
    else:
        st.info("No active emergency requests found in database.")

st.markdown("---")
st.subheader("📊 Regional Supply & Demand Insights")
c1, c2 = st.columns(2)

with c1:
    st.markdown("### Area-wise Demand Density")
    if demand_summary:
        df_summary = pd.DataFrame(demand_summary)
        st.dataframe(df_summary, use_container_width=True)
    else:
        st.info("No regional analytics dataset available.")

with c2:
    st.markdown("### Supply Deficit / Gap Breakdown")
    if demand_gap:
        df_gap = pd.DataFrame(demand_gap)
        st.dataframe(df_gap, use_container_width=True)
    else:
        st.info("Perfect Supply-Demand balance achieved! No gaps found.")

time.sleep(3)
st.rerun()



