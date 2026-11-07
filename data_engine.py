import pandas as pd
import numpy as np
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestRegressor

from models.demand import Demand
from models.inventory import Inventory
from models.supplier import Supplier

def generate_mock_data():
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    
    data = []
    categories = ['Rainy Day Comfort (Khichuri/Tea)', 'Summer Chill (Ice Cream/Cold Drinks)', 'Match Day Snacks (Chips/Popcorn)', 'Daily Groceries']
    
    for date in dates:
        temp = np.random.uniform(15, 38)
        rain_prob = np.random.uniform(0, 100)
        social_hype = np.random.uniform(0, 100)
        
        for cat in categories:
            base_sales = np.random.randint(20, 50)
            
            if cat == 'Rainy Day Comfort (Khichuri/Tea)' and rain_prob > 60:
                base_sales += (rain_prob * 1.5) + (social_hype * 0.5)
            elif cat == 'Summer Chill (Ice Cream/Cold Drinks)' and temp > 30:
                base_sales += (temp * 2.0) + (social_hype * 0.3)
            elif cat == 'Match Day Snacks (Chips/Popcorn)' and social_hype > 70:
                base_sales += (social_hype * 2.5)
                
            data.append([date, cat, temp, rain_prob, social_hype, int(base_sales)])
            
    df = pd.DataFrame(data, columns=['Date', 'Category', 'Temperature', 'Rain_Probability', 'Social_Hype', 'Sales'])
    return df

def train_predictive_model(df):
    models = {}
    for cat in df['Category'].unique():
        cat_df = df[df['Category'] == cat]
        X = cat_df[['Temperature', 'Rain_Probability', 'Social_Hype']]
        y = cat_df['Sales']
        
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        model.fit(X, y)
        models[cat] = model
    return models


DEMAND_SAMPLE_DATA = [
    {"area": "Savar", "latitude": 23.8583, "longitude": 90.2667, "category": "Food", "product_name": "Rice", "quantity": 40, "urgency": "3", "status": "pending"},
    {"area": "Ashulia", "latitude": 23.9167, "longitude": 90.3500, "category": "Water", "product_name": "Drinking Water", "quantity": 60, "urgency": "7", "status": "pending"},
    {"area": "Dhamrai", "latitude": 23.9139, "longitude": 90.2100, "category": "Medicine", "product_name": "Oral Rehydration Salts", "quantity": 25, "urgency": "9", "status": "matched"},
    {"area": "Savar", "latitude": 23.8512, "longitude": 90.2690, "category": "Emergency", "product_name": "First Aid Kit", "quantity": 15, "urgency": "10", "status": "pending"},
    {"area": "Ashulia", "latitude": 23.9211, "longitude": 90.3445, "category": "Food", "product_name": "Cooking Oil", "quantity": 30, "urgency": "5", "status": "matched"},
    {"area": "Dhamrai", "latitude": 23.9098, "longitude": 90.2162, "category": "Water", "product_name": "Water Bottles", "quantity": 80, "urgency": "6", "status": "pending"},
    {"area": "Savar", "latitude": 23.8634, "longitude": 90.2578, "category": "Medicine", "product_name": "Paracetamol", "quantity": 45, "urgency": "8", "status": "matched"},
    {"area": "Ashulia", "latitude": 23.9045, "longitude": 90.3581, "category": "Food", "product_name": "Flour", "quantity": 35, "urgency": "4", "status": "pending"},
    {"area": "Dhamrai", "latitude": 23.9225, "longitude": 90.2038, "category": "Emergency", "product_name": "Emergency Lamp", "quantity": 20, "urgency": "8", "status": "pending"},
    {"area": "Savar", "latitude": 23.8456, "longitude": 90.2743, "category": "Water", "product_name": "Water Purification Tablets", "quantity": 50, "urgency": "7", "status": "matched"},
    {"area": "Ashulia", "latitude": 23.9132, "longitude": 90.3516, "category": "Medicine", "product_name": "Antiseptic Solution", "quantity": 18, "urgency": "9", "status": "pending"},
    {"area": "Dhamrai", "latitude": 23.9180, "longitude": 90.2071, "category": "Food", "product_name": "Biscuits", "quantity": 55, "urgency": "2", "status": "matched"},
    {"area": "Savar", "latitude": 23.8675, "longitude": 90.2635, "category": "Emergency", "product_name": "Blankets", "quantity": 12, "urgency": "6", "status": "pending"},
    {"area": "Ashulia", "latitude": 23.8991, "longitude": 90.3624, "category": "Food", "product_name": "Milk", "quantity": 28, "urgency": "4", "status": "matched"},
    {"area": "Dhamrai", "latitude": 23.9066, "longitude": 90.2130, "category": "Medicine", "product_name": "Bandages", "quantity": 32, "urgency": "5", "status": "pending"},
]

SUPPLIER_SAMPLE_DATA = [
    {"supplier_name": "Savar Essentials Hub", "area": "Savar", "latitude": 23.8546, "longitude": 90.2685, "capacity": 1200, "is_active": True},
    {"supplier_name": "Ashulia Emergency Supply", "area": "Ashulia", "latitude": 23.9148, "longitude": 90.3520, "capacity": 900, "is_active": True},
    {"supplier_name": "Dhamrai Community Store", "area": "Dhamrai", "latitude": 23.9095, "longitude": 90.2112, "capacity": 750, "is_active": True},
    {"supplier_name": "Savar Health & Food Depot", "area": "Savar", "latitude": 23.8604, "longitude": 90.2601, "capacity": 1100, "is_active": True},
    {"supplier_name": "Ashulia River Supply Point", "area": "Ashulia", "latitude": 23.9022, "longitude": 90.3596, "capacity": 650, "is_active": True},
]

INVENTORY_SAMPLE_DATA = [
    (1, "Rice", "Food", 220), (1, "Drinking Water", "Water", 300), (1, "First Aid Kit", "Emergency", 50),
    (2, "Rice", "Food", 180), (2, "Cooking Oil", "Food", 120), (2, "Emergency Lamp", "Emergency", 65),
    (3, "Oral Rehydration Salts", "Medicine", 90), (3, "Paracetamol", "Medicine", 140), (3, "Blankets", "Emergency", 75),
    (4, "Bandages", "Medicine", 160), (4, "Antiseptic Solution", "Medicine", 100), (4, "Milk", "Food", 130),
    (5, "Water Bottles", "Water", 280), (5, "Water Purification Tablets", "Water", 200), (5, "Biscuits", "Food", 210),
]


def seed_sample_data(db_session: Session):
    if db_session.scalar(select(Inventory).limit(1)) is None and db_session.scalar(select(Supplier).limit(1)) is None:
        suppliers = [Supplier(**supplier_data) for supplier_data in SUPPLIER_SAMPLE_DATA]
        db_session.add_all(suppliers)
        db_session.flush()

        db_session.add_all([
            Inventory(supplier_id=supplier_id, product_name=product_name, category=category, stock_quantity=stock_quantity)
            for supplier_id, product_name, category, stock_quantity in INVENTORY_SAMPLE_DATA
        ])

    if db_session.scalar(select(Demand).limit(1)) is None:
        db_session.add_all([Demand(**demand_data) for demand_data in DEMAND_SAMPLE_DATA])

    db_session.commit()


def get_raw_demand_dataframe(db_session: Session) -> pd.DataFrame:
    demands = db_session.scalars(select(Demand)).all()
    if not demands:
        return pd.DataFrame(columns=["id", "area", "latitude", "longitude", "category", "product_name", "quantity", "urgency", "status", "created_at"])
    return pd.DataFrame([{
        "id": demand.id,
        "area": demand.area,
        "latitude": demand.latitude,
        "longitude": demand.longitude,
        "category": demand.category,
        "product_name": demand.product_name,
        "quantity": demand.quantity,
        "urgency": demand.urgency,
        "status": demand.status,
        "created_at": demand.created_at,
    } for demand in demands])


if __name__ == "__main__":
    from database import SessionLocal, init_db

    init_db()
    session = SessionLocal()
    try:
        seed_sample_data(session)
        print("Demand rows:", session.scalar(select(func.count()).select_from(Demand)))
        print("Supplier rows:", session.scalar(select(func.count()).select_from(Supplier)))
        print("Inventory rows:", session.scalar(select(func.count()).select_from(Inventory)))
    finally:
        session.close()
