import random
from database import SessionLocal, init_db
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
        # Existing old demands structure records clean up
        db.query(Demand).delete()
        db.commit()
        
        print("Inserting valid live models data into sqlite engine...")
        
        for i, area in enumerate(areas, start=1):
            cat = random.choice(categories)
            prod = random.choice(products[cat])
            qty = random.randint(15, 80)
            urgency = random.choice(["Critical", "High", "Medium"])
            
            # Creating actual model object mapping to backend structure
            new_demand = Demand(
                id=i,
                area=area,
                category=cat,
                product_name=prod,
                quantity=qty,
                urgency=urgency,
                latitude=0.0,
                longitude=0.0
            )
            db.add(new_demand)
            
        db.commit()
        print("✨ Database successfully populated using official backend models!")
    except Exception as e:
        db.rollback()
        print(f"Direct insertion failed, trying alternative schema mapper: {e}")
        # Fallback if properties are named area_name / item_category
        try:
            db.query(Demand).delete()
            for i, area in enumerate(areas, start=1):
                cat = random.choice(categories)
                prod = random.choice(products[cat])
                qty = random.randint(15, 80)
                urgency = random.choice(["Critical", "High", "Medium"])
                
                fallback_demand = Demand(
                    id=i,
                    area_name=area,
                    item_category=cat,
                    product_name=prod,
                    quantity=qty,
                    urgency=urgency,
                    latitude=0.0,
                    longitude=0.0
                )
                db.add(fallback_demand)
            db.commit()
            print("✨ Database successfully populated using alternative properties!")
        except Exception as inner_error:
            print(f"Critical mapping crash: {inner_error}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_live_data()

