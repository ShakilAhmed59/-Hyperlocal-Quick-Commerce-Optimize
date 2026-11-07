import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(
    page_title="Hyperlocal Q-Commerce Optimizer",
    page_icon=":material/emergency:",
    layout="wide",
)

st.markdown(
    """
<style>
    :root {
        color-scheme: dark;
    }
    .stApp { background: #0b1020; }
    .block-container { padding-top: 1.25rem; max-width: 1280px; }
    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #1f2937;
    }
    section[data-testid="stSidebar"] > div { padding-top: 1rem; }
    [data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #243044;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8;
        font-size: 12px;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc;
        font-size: 27px;
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        border-radius: 10px;
    }
    h1 { font-size: 22px; color: #f8fafc; }
    h2, h3 { color: #e2e8f0; }
    div[data-testid="stExpander"] {
        background: #111827;
        border-radius: 10px;
        border: 1px solid #243044;
    }
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid #243044;
        border-radius: 10px;
        overflow: hidden;
    }
    .stButton button, .stLinkButton a {
        border: 1px solid #2d3a50;
    }
    .stButton button:hover {
        border-color: #35c759;
    }
    [data-testid="stCaptionContainer"] { color: #94a3b8; }
</style>
""",
    unsafe_allow_html=True,
)

API_BASE_URL = "http://127.0.0.1:8080"
AREA_COORDINATES = {
    "Nobinagar": (23.9139, 90.2100),
    "Pollibiddut": (23.9200, 90.2500),
    "DIU Campus": (23.8759, 90.3795),
    "Eastern University Campus": (23.8106, 90.4269),
    "Uttara": (23.8764, 90.3904),
    "Mirpur 1": (23.7957, 90.3532),
    "Mirpur 2": (23.8090, 90.3638),
    "Mirpur 10": (23.8069, 90.3688),
    "Ashulia": (23.9132, 90.3516),
    "Dhamrai": (23.9180, 90.2071),
    "Savar": (23.8583, 90.2667),
}


def fetch_json(endpoint, wrapped=True):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=5)
        response.raise_for_status()
        payload = response.json()
        if wrapped and isinstance(payload, dict) and payload.get("success"):
            return payload.get("data", [])
        return payload
    except requests.RequestException:
        return []


if "dynamic_users" not in st.session_state:
    st.session_state.dynamic_users = {
        "shakilshanto899@gmail.com": {
            "password": "Shakil1024@",
            "role": "Admin",
            "area": "All",
            "name": "Md Shakil Ahmed Shanto",
            "phone": "01715233659",
        }
    }

if "riders_registry" not in st.session_state:
    st.session_state.riders_registry = [
        {"id": "R-101", "name": "Rahat Khan", "area": "Uttara", "status": "Available", "lat": 23.8740, "lon": 90.3860, "phone": "01911111111"},
        {"id": "R-102", "name": "Siam Ahmed", "area": "Mirpur 10", "status": "On Delivery", "lat": 23.8069, "lon": 90.3688, "phone": "01922222222"},
        {"id": "R-103", "name": "Tanvir Hossen", "area": "Savar", "status": "Available", "lat": 23.8583, "lon": 90.2667, "phone": "01933333333"},
    ]

weather_forecasts = ["Clear (Next 1 Hour)", "Heavy Rain Forecast (Next 1 Hour)", "Extreme Heatwave Warning", "Stormy Weather Alert"]
social_trends = ["Normal Traffic", "Facebook Viral Item Trend", "TikTok Sudden Product Demand"]
for key, default in (("weather_forecast", weather_forecasts[0]), ("social_trend", social_trends[0])):
    if key not in st.session_state:
        st.session_state[key] = default
for key, default in (("auth_success", False), ("user_role", "None"), ("assigned_area", "None"), ("user_info", {}), ("auth_mode", "Login")):
    if key not in st.session_state:
        st.session_state[key] = default

st.sidebar.markdown(
    '<div style="display:flex;align-items:center;gap:9px;padding:5px 4px 18px">'
    '<div style="width:30px;height:30px;border-radius:9px;background:#2fb344;color:white;'
    'display:flex;align-items:center;justify-content:center;font-weight:700;">HQ</div>'
    '<div><div style="font-weight:700;color:#f8fafc;">Hyperlocal</div>'
    '<div style="font-size:11px;color:#94a3b8;">Q-Commerce Optimizer</div></div></div>',
    unsafe_allow_html=True,
)

if st.session_state.auth_success:
    st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Demand Map", "Products", "Areas", "Supply Gap", "Deliveries", "Analytics", "Settings"],
        label_visibility="collapsed",
    )

st.sidebar.header("Access Control Gateway")

if not st.session_state.auth_success:
    login_col, register_col, forgot_col = st.sidebar.columns(3)
    if login_col.button("Login"):
        st.session_state.auth_mode = "Login"
    if register_col.button("Register"):
        st.session_state.auth_mode = "Register"
    if forgot_col.button("Forgot"):
        st.session_state.auth_mode = "Forgot"

    roles = ["Select Role", "Admin", "Area Manager", "Salesman"]
    if st.session_state.auth_mode == "Login":
        selected_role = st.sidebar.selectbox("Login role", roles)
        email = st.sidebar.text_input("Registered email")
        phone = st.sidebar.text_input("Registered phone number")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Secure login"):
            user = st.session_state.dynamic_users.get(email.strip())
            if user and user["password"] == password and user["phone"] == phone.strip() and user["role"] == selected_role:
                st.session_state.auth_success = True
                st.session_state.user_role = user["role"]
                st.session_state.assigned_area = user["area"]
                st.session_state.user_info = user
                st.rerun()
            else:
                st.sidebar.error("Credentials did not match.")
    elif st.session_state.auth_mode == "Register":
        role = st.sidebar.selectbox("Role", ["Area Manager", "Salesman"])
        areas = list(AREA_COORDINATES)
        area = st.sidebar.selectbox("Assigned area", areas if role == "Area Manager" else ["All"])
        name = st.sidebar.text_input("Full name")
        email = st.sidebar.text_input("Corporate email")
        phone = st.sidebar.text_input("Phone number")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Register account"):
            if not email.strip() or not password:
                st.sidebar.error("Email and password are required.")
            else:
                st.session_state.dynamic_users[email.strip()] = {
                    "password": password,
                    "role": role,
                    "area": area,
                    "name": name,
                    "phone": phone.strip(),
                }
                st.sidebar.success("Account registered.")
    else:
        email = st.sidebar.text_input("Registered email")
        phone = st.sidebar.text_input("Registered phone number")
        new_password = st.sidebar.text_input("New password", type="password")
        if st.sidebar.button("Reset password"):
            user = st.session_state.dynamic_users.get(email.strip())
            if user and user["phone"] == phone.strip():
                user["password"] = new_password
                st.sidebar.success("Password reset.")
            else:
                st.sidebar.error("Account details did not match.")
else:
    st.sidebar.markdown(f"**{st.session_state.user_info.get('name', 'User')}**")
    st.sidebar.caption(st.session_state.user_role)
    st.session_state.weather_forecast = st.sidebar.selectbox(
        "Weather forecast",
        weather_forecasts,
        index=weather_forecasts.index(st.session_state.weather_forecast),
    )
    st.session_state.social_trend = st.sidebar.selectbox(
        "Social demand trend",
        social_trends,
        index=social_trends.index(st.session_state.social_trend),
    )
    if st.sidebar.button("Logout"):
        st.session_state.auth_success = False
        st.rerun()

if not st.session_state.auth_success:
    st.warning("Access denied. Authenticate from the sidebar.")
    st.stop()

summary_rows = fetch_json("/api/demand/summary")
demand_rows = fetch_json("/api/demands", wrapped=False)
gap_rows = fetch_json("/api/demand/gap")
supplier_rows = fetch_json("/api/suppliers")

if not isinstance(summary_rows, list):
    summary_rows = []
if not isinstance(demand_rows, list):
    demand_rows = []
if not isinstance(gap_rows, list):
    gap_rows = []
if not isinstance(supplier_rows, list):
    supplier_rows = []

role = st.session_state.user_role
assigned_area = st.session_state.assigned_area
scope = None if role == "Admin" else assigned_area if role == "Area Manager" else None

if scope and scope != "All":
    demand_rows = [row for row in demand_rows if str(row.get("area", "")).lower() == scope.lower()]
    gap_rows = [row for row in gap_rows if str(row.get("area", "")).lower() == scope.lower()]
    summary_rows = [row for row in summary_rows if str(row.get("area", "")).lower() == scope.lower()]

demands_df = pd.DataFrame(demand_rows)
if demands_df.empty:
    demands_df = pd.DataFrame(columns=["area", "latitude", "longitude", "category", "product_name", "quantity", "urgency", "status"])

summary_df = pd.DataFrame([
    {
        "area": row.get("area"),
        "total_requests": row.get("total_requests", 0),
        "priority_score": row.get("priority_score", 0),
        "priority_level": row.get("priority_level", "Low"),
    }
    for row in summary_rows
])

gap_df = pd.DataFrame([
    {
        "area": row.get("area"),
        "category": row.get("category"),
        "requested_quantity": row.get("requested_quantity", 0),
        "available_stock": row.get("available_stock", 0),
        "unfulfilled_demand": row.get("unfulfilled_demand", 0),
        "critical_deficit": bool(row.get("critical_deficit", False)),
    }
    for row in gap_rows
])

inventory_rows = []
for supplier in supplier_rows:
    for item in supplier.get("inventory", []):
        inventory_rows.append({
            "supplier": supplier.get("supplier_name"),
            "area": supplier.get("area"),
            "product_name": item.get("product_name"),
            "category": item.get("category"),
            "stock_quantity": item.get("stock_quantity", 0),
        })
inventory_df = pd.DataFrame(inventory_rows)
if not inventory_df.empty and scope and scope != "All":
    inventory_df = inventory_df[inventory_df["area"].str.lower() == scope.lower()]

st.title("Hyperlocal Q-Commerce Optimizer")
st.caption(f"{role} workspace" + (f" - {scope}" if scope and scope != "All" else ""))

if not demand_rows:
    st.error("The backend API is unavailable or no demand data is present. Start the FastAPI service on port 8080.")

total_demand = int(pd.to_numeric(demands_df.get("quantity", pd.Series(dtype=float)), errors="coerce").fillna(0).sum())
area_count = demands_df["area"].nunique() if not demands_df.empty else 0
gap_count = int(pd.to_numeric(gap_df.get("unfulfilled_demand", pd.Series(dtype=float)), errors="coerce").fillna(0).gt(0).sum()) if not gap_df.empty else 0
critical_count = int(pd.to_numeric(demands_df.get("urgency", pd.Series(dtype=float)), errors="coerce").fillna(0).ge(7).sum()) if not demands_df.empty else 0

metric_columns = st.columns(4)
metric_columns[0].metric("Total demand units", total_demand)
metric_columns[1].metric("Areas", area_count)
metric_columns[2].metric("Supply gaps", gap_count)
metric_columns[3].metric("Critical requests", critical_count)

st.subheader("Live demand map")
map_center = (23.8759, 90.3795)
live_map = folium.Map(
    location=map_center,
    zoom_start=10,
    tiles="CartoDB dark_matter",
    attr="CartoDB",
)
for _, demand in demands_df.iterrows():
    area = str(demand.get("area", "Unknown"))
    latitude = float(demand.get("latitude", 0) or 0)
    longitude = float(demand.get("longitude", 0) or 0)
    if latitude == 0 or longitude == 0:
        latitude, longitude = AREA_COORDINATES.get(area, map_center)
    quantity = pd.to_numeric(pd.Series([demand.get("quantity", 0)]), errors="coerce").fillna(0).iloc[0]
    category = demand.get("category", "General")
    folium.CircleMarker(
        location=[latitude, longitude],
        radius=min(20, max(5, float(quantity) / 3)),
        color="#d97706" if str(demand.get("urgency", 0)).replace(".", "", 1).isdigit() and float(demand.get("urgency", 0)) >= 7 else "#2563eb",
        fill=True,
        fill_opacity=0.7,
        tooltip=f"{area}: {demand.get('product_name')} - {quantity} units ({category})",
    ).add_to(live_map)
st_folium(live_map, width=None, height=420, returned_objects=[])

st.subheader("Product demand")
product_categories = ["All", "Food", "Water", "Medicine", "Essentials"]
selected_category = st.segmented_control("Category", product_categories, default="All")
category_demand = demands_df.copy()
if selected_category != "All":
    category_demand = category_demand[
        category_demand["category"].astype(str).str.lower() == selected_category.lower()
    ]

product_summary = category_demand.groupby("product_name", as_index=False).agg(
    quantity=("quantity", "sum"),
    requests=("product_name", "count"),
    areas=("area", "nunique"),
) if not category_demand.empty else pd.DataFrame(columns=["product_name", "quantity", "requests", "areas"])
st.dataframe(product_summary.sort_values("quantity", ascending=False), hide_index=True, width="stretch")

area_chart = pd.DataFrame()
if not summary_df.empty:
    area_chart = summary_df.copy()
    area_chart["total_requests"] = pd.to_numeric(area_chart["total_requests"], errors="coerce").fillna(0)
    st.subheader("Area-wise demand")
    st.bar_chart(area_chart, x="area", y="total_requests", color="#2563eb")

st.subheader("Area demand and quantity")
if not demands_df.empty:
    area_quantity = demands_df.groupby(["area", "category"], as_index=False)["quantity"].sum()
    st.dataframe(area_quantity.sort_values(["area", "quantity"], ascending=[True, False]), hide_index=True, width="stretch")
else:
    st.info("No area demand data is available.")

st.subheader("Supply-demand gap")
if gap_df.empty:
    st.info("No supply-demand gap data is available.")
else:
    gap_display = gap_df.copy()
    gap_display["status"] = gap_display["critical_deficit"].map({True: "Critical deficit", False: "Covered"})
    st.dataframe(
        gap_display[["area", "category", "requested_quantity", "available_stock", "unfulfilled_demand", "status"]],
        hide_index=True,
        width="stretch",
    )
    gap_chart = gap_display.groupby("area", as_index=False)[["requested_quantity", "available_stock", "unfulfilled_demand"]].sum()
    st.bar_chart(gap_chart, x="area", y=["requested_quantity", "available_stock", "unfulfilled_demand"])

with st.expander("Inventory and suppliers"):
    if inventory_df.empty:
        st.info("No supplier inventory data is available.")
    else:
        st.dataframe(inventory_df.sort_values(["area", "category", "product_name"]), hide_index=True, width="stretch")
