from typing import Literal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from backend.predictor import predict_trip_safety

app = FastAPI(
    title="Vehicle Maintenance Predictor API",
    version="1.0.0",
    description="API de maintenance prédictive pour flottes de transport et suivi de santé du véhicule.",
    docs_url="/docs",
    redoc_url="/redoc",
)


class TripCheckRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

    trip_distance_km: int = Field(default=240, gt=0, description="Distance prévue du trajet en kilomètres")
    km_since_last_oil_change: int = Field(..., ge=0, description="Kilométrage depuis la dernière vidange")
    engine_temp_celsius: float = Field(..., ge=0, le=150, description="Température moteur en °C")
    oil_level_percent: float = Field(..., ge=0, le=100, description="Niveau d'huile en pourcentage")
    passenger_load_percent: float = Field(..., ge=0, le=100, description="Charge du véhicule en pourcentage")


class TripCheckResponse(BaseModel):
    status: Literal["SAFE", "WARNING", "CRITICAL_RISK"]
    trip_distance_km: int
    remaining_autonomy_km: int
    predicted_breakdown_km: int | None = None
    critical_location: str | None = None
    recommendation: str
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "API de Maintenance Prédictive Opérationnelle",
        "version": app.version,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "vehicle-maintenance-predictor"}


@app.post("/predict-trip", response_model=TripCheckResponse, status_code=status.HTTP_200_OK)
def check_trip(data: TripCheckRequest):
    try:
        result = predict_trip_safety(
            trip_distance_km=data.trip_distance_km,
            km_since_last_oil_change=data.km_since_last_oil_change,
            engine_temp_celsius=data.engine_temp_celsius,
            oil_level_percent=data.oil_level_percent,
            passenger_load_percent=data.passenger_load_percent,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(exc), "message": "Les données du trajet sont invalides."},
        ) from exc

    response = TripCheckResponse(
        status=result["status"],
        trip_distance_km=result["trip_distance_km"],
        remaining_autonomy_km=result["remaining_autonomy_km"],
        predicted_breakdown_km=result.get("predicted_breakdown_km"),
        critical_location=result.get("critical_location"),
        recommendation=result["recommendation"],
        message=result["message"],
    )
    return response
