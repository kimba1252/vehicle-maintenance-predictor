"""Pydantic models for request/response validation."""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class TripCheckRequest(BaseModel):
    """Request model for trip prediction."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "trip_distance_km": 240,
                "km_since_last_oil_change": 4200,
                "engine_temp_celsius": 96,
                "oil_level_percent": 65,
                "passenger_load_percent": 80,
            }
        },
    )

    trip_distance_km: int = Field(
        default=240,
        gt=0,
        description="Distance prévue du trajet en kilomètres",
    )
    km_since_last_oil_change: int = Field(
        ...,
        ge=0,
        description="Kilométrage depuis la dernière vidange (km)",
    )
    engine_temp_celsius: float = Field(
        ...,
        ge=0,
        le=150,
        description="Température moteur en degrés Celsius",
    )
    oil_level_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Niveau d'huile en pourcentage (%)",
    )
    passenger_load_percent: float = Field(
        ...,
        ge=0,
        le=100,
        description="Charge du véhicule en pourcentage (%)",
    )


class TripCheckResponse(BaseModel):
    """Response model for trip prediction."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "WARNING",
                "trip_distance_km": 240,
                "remaining_autonomy_km": 170,
                "predicted_breakdown_km": None,
                "critical_location": None,
                "recommendation": "Trajet possible, prévoir révision dès l'arrivée.",
                "message": "Le véhicule est viable pour le trajet, mais une maintenance préventive est recommandée.",
                "safety_margin_km": 50,
            }
        }
    )

    status: Literal["SAFE", "WARNING", "CRITICAL_RISK"]
    trip_distance_km: int
    remaining_autonomy_km: int
    predicted_breakdown_km: Optional[int] = None
    critical_location: Optional[str] = None
    recommendation: str
    message: str
    safety_margin_km: float


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str
    service: str
    version: str


class ErrorResponse(BaseModel):
    """Response model for errors."""

    error: str
    message: str
    status_code: int
