import random
import time
from database import SessionLocal
from models.demand import Demand

areas = [
    "Nobinagar", "Pollibiddut", "DIU Campus", "Eastern University Campus", 
    "Uttara", "Mirpur 1", "Mirpur 2", "Mirpur 10", "Ashulia", "Dhamrai", "Savar"
]
categories = ["Food", "Medicine", "Water", "Emergency"]
products = {
    "Food": ["Rice Bag", "Dry Snacks", "Baby Food"],
    "Medicine": ["Antiseptic Solution", "Oral Rehydration Salts", "Paracetamol Syrup"],
    "Water": ["Drinking Water (5L)", "Water Purification Tablets"],
    "Emergency": ["Emergency Lamp", "Blankets", "First Aid Kit"]
}

def populate_live_data():
    db = SessionLocal()
    try:
        db.query(Demand).delete()
        for i, area in enumerate(areas, start=1):
            cat = random.choice(categories)
            prod = random.choice(products[cat])
            qty = random.randint(10, 100)
            urgency = random.choice(["Critical", "High", "Medium"])
            
            new_demand = Demand(
                id=i, area=area, category=cat, product_name=prod,
                quantity=qty, urgency=urgency, latitude=0.0, longitude=0.0
            )
            db.add(new_demand)
        db.commit()
        print("⚡ Live Database updated with Predictive Stream Data...")
    except Exception as e:
        db.rollback()
        print(f"Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Running Real-time 1-Sec Hyperlocal Demand Streamer...")
    while True:
        populate_live_data()
        time.sleep(1)



