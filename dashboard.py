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

# --- CORE USER DATABASE & STATE MANAGEMENT ---
if "dynamic_users" not in st.session_state:
    st.session_state.dynamic_users = {
        "shakilshanto899@gmail.com": {"password": "Shakil1024@", "role": "Admin", "area": "All", "name": "Shakil Ahmed (Super Admin)", "phone": "01715233659"}
    }

# --- RIDERS REGISTRY STORAGE ---
if "riders_registry" not in st.session_state:
    st.session_state.riders_registry = [
        {"id": "R-101", "name": "Rahat Khan", "area": "Uttara", "status": "Available", "lat": 23.8740, "lon": 90.3860, "phone": "01911111111"},
        {"id": "R-102", "name": "Siam Ahmed", "area": "Mirpur 10", "status": "On Delivery", "lat": 23.8069, "lon": 90.3688, "phone": "01922222222"},
        {"id": "R-103", "name": "Tanvir Hossen", "area": "Savar", "status": "Available", "lat": 23.8583, "lon": 90.2667, "phone": "01933333333"}
    ]

weather_conditions = ["⛈️ Heavy Rain / Flood Risk", "☀️ Extreme Heatwave", "🌤️ Normal Weather"]
if 'current_weather' not in st.session_state:
    st.session_state.current_weather = "🌤️ Normal Weather"

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
                else: st.sidebar.error("❌ Mismatched Credentials!")
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
                st.sidebar.success("✨ Registered!")

    elif st.session_state.auth_mode == "Forgot":
        f_email = st.sidebar.text_input("Enter Email")
        f_phone = st.sidebar.text_input("Enter Phone")
        f_new_pass = st.sidebar.text_input("New Password", type="password")
        if st.sidebar.button("Reset Credentials"):
            email_clean = f_email.strip()
            if email_clean in st.session_state.dynamic_users and st.session_state.dynamic_users[email_clean]["phone"] == f_phone.strip():
                st.session_state.dynamic_users[email_clean]["password"] = f_new_pass
                st.sidebar.success("🔒 Reset Successful!")
            else: st.sidebar.error("❌ Invalid Phone or Email match failed.")

else:
    st.sidebar.success(f"Active Session: **{st.session_state.user_info['name']}**")
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌤️ Weather Analytics Control")
    st.session_state.current_weather = st.sidebar.selectbox("Simulate System Weather:", weather_conditions, index=weather_conditions.index(st.session_state.current_weather))
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.auth_success = False
        st.session_state.user_role = "None"
        st.rerun()

if not st.session_state.auth_success:
    st.warning("⚠️ Access Denied. Please authenticate via the Sidebar Gateway.")
    st.stop()

# --- DATA NORMALIZATION ENGINE ---
raw_summary = fetch_api_data("/api/demand/summary")
raw_demands = fetch_api_data("/api/demand/gap")

demand_summary = []
if raw_summary:
    for item in raw_summary:
        demand_summary.append({
            "area_name": item.get("area_name") or item.get("area") or "Unknown Zone",
            "total_requests": item.get("total_requests") or item.get("quantity") or 0
        })

emergency_demands = []
if raw_demands:
    for item in raw_demands:
        area_str = item.get("area_name") or item.get("area") or "Unknown"
        cat_str = item.get("item_category") or item.get("category") or "General"
        prod_str = item.get("product_name") or item.get("item_name") or "Product SKU"
        qty_int = int(item.get("quantity") or item.get("requested_quantity") or item.get("qty") or 0)
        stock_int = int(item.get("available_stock") or item.get("stock_level") or random.randint(5, 30))
        rate_int = int(item.get("product_rate") or random.randint(150, 450) if cat_str == "Food" else random.randint(20, 120))
        
        emergency_demands.append({
            "area": area_str,
            "category": cat_str,
            "product_name": prod_str,
            "quantity": qty_int,
            "rate_bdt": rate_int,
            "stock_level": stock_int,
            "latitude": item.get("latitude") or item.get("lat") or 0.0,
            "longitude": item.get("longitude") or item.get("lon") or 0.0
        })

is_admin = st.session_state.user_role == "Admin"
is_area_manager = st.session_state.user_role == "Area Manager"
manager_assigned_zone = st.session_state.assigned_area

st.title("🚨 Hyperlocal Q-Commerce Optimizer & Emergency Supply Network")
st.markdown(f"Welcome back, **{st.session_state.user_info['name']}**")

# --- WEATHER NOTIFICATIONS ---
st.subheader("🔔 Intelligent Real-time System Notifications & Actionable Weather Alerts")
notifications = []

if emergency_demands:
    for item in emergency_demands:
        if item["quantity"] > 15:
            notifications.append(f"🚨 **High Emergency Demand Alert:** `{item['area']}` requires **{item['quantity']} units** of **{item['product_name']}** (Price: ৳{item['rate_bdt']})! Available Stock: {item['stock_level']} units.")
        if "Heavy Rain" in st.session_state.current_weather and item["category"] == "Medicine":
            notifications.append(f"🌧️ **[STOCK-IN ALERTVIEW]** Heavy Rain! Waterborne risk in `{item['area']}`. **STOCK-IN** more `{item['product_name']}`.")
        elif "Heatwave" in st.session_state.current_weather and item["category"] == "Water":
            notifications.append(f"🔥 **[STOCK-OUT SUGGESTION]** Heatwave alert! Dehydration risk in `{item['area']}`. **STOCK-OUT** `{item['product_name']}`.")

if notifications:
    for note in notifications[:2]: st.warning(note)
else:
    st.info("✅ System operations parameters normal. All regional nodes balanced.")

st.markdown("---")

# --- ADMIN PANEL ---
if is_admin:
    st.subheader("👑 Admin Security & User Registry Control")
    adm_col1, adm_col2 = st.columns(2)
    with adm_col1:
        st.markdown("### ➕ Register New Subordinate Directly")
        with st.form("admin_create_user_form", clear_on_submit=True):
            new_role = st.selectbox("Assign Role Architecture", ["Area Manager", "Sales Manager"])
            available_areas = ["Uttara", "Mirpur 1", "Mirpur 2", "Mirpur 10", "Ashulia", "Dhamrai", "Savar", "Nobinagar", "Pollibiddut", "DIU Campus", "Eastern University Campus"]
            new_area = st.selectbox("Assign Area Scope", available_areas if new_role == "Area Manager" else ["All"])
            new_name = st.text_input("Full Profile Name")
            new_email = st.text_input("Corporate Email Address")
            new_phone = st.text_input("Contact Phone Number")
