import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
import time
import random

st.set_page_config(
    page_title="Hyperlocal Q-Commerce Optimizer",
    page_icon="🚨",
    layout="wide"
)

API_BASE_URL = "http://127.0.0.1:8080"

def fetch_api_data(endpoint):
    try:
        res = requests.get(f"{API_BASE_URL}{endpoint}")
        if res.status_code == 200 and res.json().get("success"):
            return res.json().get("data", [])
    except Exception:
        return []
    return []

if "dynamic_users" not in st.session_state:
    st.session_state.dynamic_users = {
        "shakilshanto899@gmail.com": {
            "password": "Shakil1024@", 
            "role": "Admin", 
            "area": "All", 
            "name": "Md Shakil Ahmed Shanto (Super Admin)", 
            "phone": "01715233659"
        }
    }

if "riders_registry" not in st.session_state:
    st.session_state.riders_registry = [
        {"id": "R-101", "name": "Rahat Khan", "area": "Uttara", "status": "Available", "lat": 23.8740, "lon": 90.3860, "phone": "01911111111"},
        {"id": "R-102", "name": "Siam Ahmed", "area": "Mirpur 10", "status": "On Delivery", "lat": 23.8069, "lon": 90.3688, "phone": "01922222222"},
        {"id": "R-103", "name": "Tanvir Hossen", "area": "Savar", "status": "Available", "lat": 23.8583, "lon": 90.2667, "phone": "01933333333"}
    ]

weather_forecasts = ["🌤️ Clear (Next 1 Hour)", "⛈️ Heavy Rain Forecast (Next 1 Hour)", "☀️ Extreme Heatwave Warning", "🌪️ Stormy Weather Alert"]
social_trends = ["📉 Normal Traffic", "🔥 Facebook Viral Item Trend", "🚀 TikTok Sudden Product Demand"]

if 'weather_forecast' not in st.session_state: st.session_state.weather_forecast = "🌤️ Clear (Next 1 Hour)"
if 'social_trend' not in st.session_state: st.session_state.social_trend = "📉 Normal Traffic"

if 'auth_success' not in st.session_state: st.session_state.auth_success = False
if 'user_role' not in st.session_state: st.session_state.user_role = "None"
if 'assigned_area' not in st.session_state: st.session_state.assigned_area = "None"
if 'user_info' not in st.session_state: st.session_state.user_info = {}
if 'auth_mode' not in st.session_state: st.session_state.auth_mode = "Login"

st.sidebar.header("🔐 Access Control Gateway")

if not st.session_state.auth_success:
    m_col1, m_col2, m_col3 = st.sidebar.columns(3)
    with m_col1:
        if st.button("🔑 Login"): st.session_state.auth_mode = "Login"
    with m_col2:
        if st.button("📝 Register"): st.session_state.auth_mode = "Register"
    with m_col3:
        if st.button("🔄 Forgot"): st.session_state.auth_mode = "Forgot"

    st.sidebar.markdown(f"**Current Action:** `{st.session_state.auth_mode} System`")

    if st.session_state.auth_mode == "Login":
        selected_role = st.sidebar.selectbox("Select Your Login Role:", ["Select Role", "Admin", "Area Manager", "Sales Manager"])
        log_email = st.sidebar.text_input("Registered Email Address")
        log_phone = st.sidebar.text_input("Registered Phone Number")
        log_pass = st.sidebar.text_input("Enter Account Password", type="password")
        
        if st.sidebar.button("Execute Secure Login"):
            email_clean = log_email.strip()
            phone_clean = log_phone.strip()
            if email_clean in st.session_state.dynamic_users:
                user = st.session_state.dynamic_users[email_clean]
                if user["password"] == log_pass and user["phone"] == phone_clean and user["role"] == selected_role:
                    st.session_state.auth_success = True
                    st.session_state.user_role = user["role"]
                    st.session_state.assigned_area = user["area"]
                    st.session_state.user_info = user
                    st.rerun()
                else: st.sidebar.error("❌ Credentials Mismatched!")
            else: st.sidebar.error("❌ Record not found!")

    elif st.session_state.auth_mode == "Register":
        reg_role = st.sidebar.selectbox("Choose Role Architecture", ["Area Manager", "Sales Manager"])
        available_areas = ["Uttara", "Mirpur 1", "Mirpur 2", "Mirpur 10", "Ashulia", "Dhamrai", "Savar", "Nobinagar", "Pollibiddut", "DIU Campus", "Eastern University Campus"]
        reg_area = st.sidebar.selectbox("Assigned Area Scope", available_areas if reg_role == "Area Manager" else ["All"])
        reg_name = st.sidebar.text_input("Full Profile Name")
        reg_email = st.sidebar.text_input("Corporate Email Address")
        reg_phone = st.sidebar.text_input("Contact Phone Number")
        reg_pass = st.sidebar.text_input("Set Custom Access Password", type="password")
        if st.sidebar.button("Register Account"):
            email_clean = reg_email.strip()
            if not email_clean or not reg_pass:
                st.sidebar.error("❌ Email and Password cannot be empty!")
            else:
                st.session_state.dynamic_users[email_clean] = {"password": reg_pass, "role": reg_role, "area": reg_area, "name": reg_name, "phone": reg_phone.strip()}
                st.sidebar.success("✨ Registered! Switch to Login Mode.")

    elif st.session_state.auth_mode == "Forgot":
        f_email = st.sidebar.text_input("Enter Registered Email Block")
        f_phone = st.sidebar.text_input("Enter Registered Phone Block")
        f_new_pass = st.sidebar.text_input("Enter New Password Variant", type="password")
        if st.sidebar.button("Reset Security Credentials"):
            email_clean = f_email.strip()
            if email_clean in st.session_state.dynamic_users and st.session_state.dynamic_users[email_clean]["phone"] == f_phone.strip():
                st.session_state.dynamic_users[email_clean]["password"] = f_new_pass
                st.sidebar.success("🔒 Password successfully reset! Please login now.")
                st.rerun()
            else:
                st.sidebar.error("❌ Profile identity match failed!")

else:
    st.sidebar.success(f"Active Session: **{st.session_state.user_info['name']}**")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 AI Predictive Input Stream")
    st.session_state.weather_forecast = st.sidebar.selectbox("1-Hour Weather Forecast:", weather_forecasts, index=weather_forecasts.index(st.session_state.weather_forecast) if st.session_state.weather_forecast in weather_forecasts else 0)
    st.session_state.social_trend = st.sidebar.selectbox("Social Media Trend Tracker:", social_trends, index=social_trends.index(st.session_state.social_trend))
    if st.sidebar.button("🚪 Logout"):
        st.session_state.auth_success = False
        st.rerun()

if not st.session_state.auth_success:
    st.warning("⚠️ Access Denied. Please authenticate via the Sidebar Control Gateway.")
    st.stop()

raw_summary = fetch_api_data("/api/demand/summary")
raw_demands = fetch_api_data("/api/demand/gap")
default_areas = ["Nobinagar", "Pollibiddut", "DIU Campus", "Eastern University Campus", "Uttara", "Mirpur 1", "Mirpur 2", "Mirpur 10", "Ashulia", "Dhamrai", "Savar"]

demand_summary = []
if raw_summary:
    for item in raw_summary:
        demand_summary.append({
            "area_name": item.get("area_name") or item.get("area") or "Unknown Zone",
            "total_requests": item.get("total_requests") or item.get("quantity") or random.randint(1, 10)
        })
else:
    for area in default_areas:
        demand_summary.append({"area_name": area, "total_requests": random.randint(1, 10)})

emergency_demands = []
if raw_demands:
    for item in raw_demands:
        area_str = item.get("area_name") or item.get("area") or "Unknown"
        cat_str = item.get("item_category") or item.get("category") or "General"
        prod_str = item.get("product_name") or item.get("item_name") or "Product SKU"
        qty_int = int(item.get("quantity") or item.get("qty") or random.randint(10, 80))
        emergency_demands.append({
            "area": area_str, "category": cat_str, "product_name": prod_str, "quantity": qty_int,
            "rate_bdt": random.randint(150, 450) if cat_str == "Food" else random.randint(20, 120),
            "stock_level": random.randint(0, 400), "latitude": item.get("latitude") or item.get("lat") or 0.0, "longitude": item.get("longitude") or item.get("lon") or 0.0
        })
else:
    for idx, area in enumerate(default_areas):
        cat_choice = ["Food", "Medicine", "Water", "Emergency"][idx % 4]
        emergency_demands.append({
            "area": area, "category": cat_choice, "product_name": f"{cat_choice} Supply SKU", "quantity": random.randint(15, 80),
            "rate_bdt": random.randint(20, 300), "stock_level": random.randint(0, 350), "latitude": 0.0, "longitude": 0.0
        })

is_admin = st.session_state.user_role == "Admin"
is_area_manager = st.session_state.user_role == "Area Manager"
manager_assigned_zone = st.session_state.assigned_area

st.title("🚨 Hyperlocal Q-Commerce Optimizer & Emergency Supply Network")

st.subheader("🔔 Real-Time AI System Ingestion & Automated Dark Store Alerts")
notifications = []
if emergency_demands:
    for item in emergency_demands:
        if item["quantity"] > 15:
            notifications.append(f"🚨 **High Emergency Demand Alert:** `{item['area']}` requires **{item['quantity']} units** of **{item['product_name']}**! Current Warehouse Stock: {item['stock_level']} units.")
        
        # সুবিন্যস্ত এরর-ফ্রি ফ্ল্যাট অ্যালার্ট মেকানিজম
        is_heavy_rain = "Heavy Rain" in st.session_state.weather_forecast and item["category"] == "Medicine"
        is_social_viral = "Facebook Viral" in st.session_state.social_trend and item["category"] == "Food"
        
        if is_heavy_rain:
            notifications.append(f"🌧️ **AI Predictive Restock Alert:** 1-Hour Rain Forecasted! Predictive demand score spiked for **{item['product_name']}** in `{item['area']}`. **Auto-Restock Initiated** to Dark Store.")

