import streamlit as st
import pandas as pd
import plotly.express as px
from data_engine import generate_mock_data, train_predictive_model

st.set_page_config(page_title="Hyperlocal Q-Commerce Optimizer", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #FF4B4B; text-align: center; margin-bottom: 20px; }
    .metric-box { background-color: #262730; padding: 15px; border-radius: 10px; border-left: 5px solid #FF4B4B; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🚀 Predictive Micro-Market Inventory Optimization for Hyperlocal Quick-Commerce</p>', unsafe_allow_html=True)

@st.cache_data
def load_system():
    df = generate_mock_data()
    models = train_predictive_model(df)
    return models

models = load_system()

st.sidebar.header("🎛️ Live Simulation Controls")
st.sidebar.info("Adjust the sliders below to dynamically change the micro-market demand conditions in real-time.")

location = st.sidebar.selectbox("📍 Select Micro-Market / Dark Store", ["Dhanmondi (Dhaka)", "Uttara (Dhaka)", "Gulshan (Dhaka)"])

st.sidebar.markdown("---")
st.sidebar.subheader("🌧️ Hyperlocal Weather Forecast")
sim_temp = st.sidebar.slider("Temperature (°C)", min_value=15, max_value=40, value=28)
sim_rain = st.sidebar.slider("Rain Probability (%)", min_value=0, max_value=100, value=10)

st.sidebar.markdown("---")
st.sidebar.subheader("📱 Social Media Listening Score")
sim_social = st.sidebar.slider("Social Hype / Trend Score", min_value=0, max_value=100, value=30)

predictions = {}
for cat, model in models.items():
    pred_input = pd.DataFrame([[sim_temp, sim_rain, sim_social]], columns=['Temperature', 'Rain_Probability', 'Social_Hype'])
    pred_sales = model.predict(pred_input)
predictions[cat] = int(pred_sales[0])


st.subheader("⚠️ Real-Time Stock Optimization Alerts")
if sim_rain > 70 and sim_social > 60:
    st.error(f"🚨 **HIGH ALERT for {location}:** Heavy Rain expected & High Social Media Hype! Stock up on **Rainy Day Comfort Items** immediately to prevent stock-outs!")
elif sim_temp > 33:
    st.warning(f"☀️ **WEATHER ALERT:** High temperature detected. Automatically increasing shelf-space for **Summer Chill** products by 40%.")
elif sim_social > 80:
    st.success(f"🔥 **TRENDING ALERT:** Extreme Social Media Hype detected in {location}. Optimizing local rider dispatch routes.")
else:
    st.info("✅ Current inventory levels are optimized. System is actively listening to live market feeds.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔮 Predicted Demand & Optimal Shelf Allocation")
    
    pred_df = pd.DataFrame(list(predictions.items()), columns=['Category', 'Recommended Stock (Units)'])
    
    total_capacity = 400
    pred_df['Shelf Allocation %'] = ((pred_df['Recommended Stock (Units)'] / total_capacity) * 100).round(1)
    
    fig = px.bar(pred_df, x='Category', y='Recommended Stock (Units)', color='Category', 
                 text='Recommended Stock (Units)', title="Next-Hour Stock Recommendations",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(template="plotly_dark", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📦 Dark Store Shelf Space Optimization Metric")
    
    fig_pie = px.pie(pred_df, values='Shelf Allocation %', names='Category', 
                     title="Optimal Space Distribution Matrix",
                     hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
    fig_pie.update_layout(template="plotly_dark")
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("📋 Live Inventory Procurement Ledger")
st.dataframe(pred_df, use_container_width=True)

