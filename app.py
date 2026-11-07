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
from services.supplier_matcher import assign_supplier_to_demand, find_matching_suppliers
from services.report_generator import generate_csv_reports, generate_pdf_summary_report

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


@app.on_event("startup")
def initialize_database():
    init_db()


@app.post("/api/demands", status_code=201, tags=["Demand Management"])
def create_demand(payload: DemandCreate, db: Session = Depends(get_db)):
    demand = Demand(**payload.model_dump())
    db.add(demand)
    db.commit()
    db.refresh(demand)
    return demand


@app.get("/api/demands", tags=["Demand Management"])
def list_demands(area: str | None = None, category: str | None = None, status: str | None = None, db: Session = Depends(get_db)):
    statement = select(Demand)
    if area:
        statement = statement.where(Demand.area.ilike(f"%{area}%"))
    if category:
        statement = statement.where(Demand.category.ilike(f"%{category}%"))
    if status:
        statement = statement.where(Demand.status == status)
    return db.scalars(statement).all()


@app.get("/api/demands/areas", tags=["Demand Management"])
def demand_areas(db: Session = Depends(get_db)):
    return get_area_demand_summary(db)


@app.get("/api/demands/emergency", tags=["Demand Management"])
def emergency_demands(db: Session = Depends(get_db)):
    return get_emergency_demands(db)


@app.post("/api/suppliers", status_code=201, tags=["Suppliers"])
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    supplier = Supplier(**payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@app.get("/api/suppliers", tags=["Suppliers"])
def list_suppliers(db: Session = Depends(get_db)):
    suppliers = db.scalars(select(Supplier).where(Supplier.is_active.is_(True))).all()
    result = []
    for supplier in suppliers:
        inventory = db.scalars(select(Inventory).where(Inventory.supplier_id == supplier.id)).all()
        result.append({
            "id": supplier.id,
            "supplier_name": supplier.supplier_name,
            "area": supplier.area,
            "latitude": supplier.latitude,
            "longitude": supplier.longitude,
            "capacity": supplier.capacity,
            "is_active": supplier.is_active,
            "inventory": [{
                "id": item.id,
                "product_name": item.product_name,
                "category": item.category,
                "stock_quantity": item.stock_quantity,
            } for item in inventory],
        })
    return result


@app.post("/api/matching/find", tags=["Supplier Matching"])
def find_matches(payload: dict, db: Session = Depends(get_db)):
    demand_id = payload.get("demand_id")
    if demand_id is None:
        raise HTTPException(status_code=422, detail="demand_id is required")
    return find_matching_suppliers(int(demand_id), db, float(payload.get("max_distance_km", 15.0)))


@app.post("/api/matching/assign", tags=["Supplier Matching"])
def assign_match(payload: dict, db: Session = Depends(get_db)):
    try:
        return assign_supplier_to_demand(int(payload["demand_id"]), int(payload["supplier_id"]), db)
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/location/distance", tags=["Location Services"])
def road_distance(payload: dict):
    required = {"lat1", "lon1", "lat2", "lon2"}
    if not required.issubset(payload):
        raise HTTPException(status_code=422, detail="lat1, lon1, lat2 and lon2 are required")
    return get_road_distance_and_duration(payload["lat1"], payload["lon1"], payload["lat2"], payload["lon2"])


@app.get("/api/analytics/supply-gap", tags=["Analytics"])
def analytics_supply_gap(db: Session = Depends(get_db)):
    return get_supply_demand_gap(db)


@app.post("/api/reports/generate", tags=["Reports"])
def generate_reports(db: Session = Depends(get_db)):
    return {"csv_reports": generate_csv_reports(db), "pdf_report": generate_pdf_summary_report(db)}


@app.get("/api/reports/download/pdf", tags=["Reports"])
def download_pdf():
    report_path = Path("reports/pdf/hyperlocal_summary_report.pdf")
    if not report_path.is_file():
        raise HTTPException(status_code=404, detail="PDF report has not been generated")
    return FileResponse(report_path, media_type="application/pdf", filename=report_path.name)


@app.get("/api/reports/download/csv/{report_name}", tags=["Reports"])
def download_csv(report_name: str):
    allowed = {"area_demand_report.csv", "emergency_priority_report.csv", "supply_gap_report.csv", "supplier_matching_report.csv"}
    report_path = Path("reports/csv") / report_name
    if report_name not in allowed or not report_path.is_file():
        raise HTTPException(status_code=404, detail="CSV report was not found")
    return FileResponse(report_path, media_type="text/csv", filename=report_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)




