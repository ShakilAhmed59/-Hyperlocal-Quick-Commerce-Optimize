from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db, init_db
from models.demand import Demand
from models.inventory import Inventory
from models.supplier import Supplier
from schemas.demand_schema import DemandCreate
from schemas.supplier_schema import SupplierCreate

from services.demand_analyzer import (
    get_area_demand_summary,
    get_emergency_demands,
    get_supply_demand_gap,
)
from services.location_service import get_road_distance_and_duration

app = FastAPI(
    title="Hyperlocal Q-Commerce Optimizer API",
    description="Emergency Supply Detection & Smart Delivery Router Backend",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "status": "Online",
        "project": "Hyperlocal Q-Commerce Optimizer Backend"
    }

@app.get("/api/demand/summary", tags=["Demand Analytics"])
def read_demand_summary(db: Session = Depends(get_db)):
    try:
        return {"success": True, "data": get_area_demand_summary(db)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/demand/emergency", tags=["Demand Analytics"])
def read_emergency_demands(db: Session = Depends(get_db)):
    try:
        return {"success": True, "data": get_emergency_demands(db)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/demand/gap", tags=["Demand Analytics"])
def read_supply_demand_gap(db: Session = Depends(get_db)):
    try:
        return {"success": True, "data": get_supply_demand_gap(db)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/location/distance", tags=["Location Services"])
def calculate_distance(start_lat: float, start_lon: float, end_lat: float, end_lon: float):
    try:
        result = get_road_distance_and_duration(start_lat, start_lon, end_lat, end_lon)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)




