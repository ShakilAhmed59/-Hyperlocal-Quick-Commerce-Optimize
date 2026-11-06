import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

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
