from fastapi import FastAPI
from pydantic import BaseModel
from backend.predictor import predict_trip_safety

app = FastAPI(
    title="Vehicle Maintenance Predictor API",
    description="API de maintenance prédictive pour flottes de transport"
)

class TripCheckRequest(BaseModel):
    trip_distance_km: int = 240
    km_since_last_oil_change: int
    engine_temp_celsius: float
    oil_level_percent: float
    passenger_load_percent: float

@app.get("/")
def home():
    return {"status": "online", "message": "API de Maintenance Prédictive Opérationnelle"}

@app.post("/predict-trip")
def check_trip(data: TripCheckRequest):
    return predict_trip_safety(
        trip_distance_km=data.trip_distance_km,
        km_since_last_oil_change=data.km_since_last_oil_change,
        engine_temp_celsius=data.engine_temp_celsius,
        oil_level_percent=data.oil_level_percent,
        passenger_load_percent=data.passenger_load_percent
    )
