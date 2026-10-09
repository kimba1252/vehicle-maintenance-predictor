"""Prediction endpoints."""

import logging

from fastapi import APIRouter, HTTPException, status

from backend.models import TripCheckRequest, TripCheckResponse
from backend.services.predictor import predictor

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/predict", tags=["predictions"])


@router.post("/trip", response_model=TripCheckResponse, status_code=status.HTTP_200_OK)
def predict_trip(data: TripCheckRequest):
    """Predict trip safety based on vehicle metrics.

    This endpoint analyzes the vehicle's condition (oil level, temperature, load)
    and predicts if it's safe to embark on the trip.

    Args:
        data: Trip check request with vehicle metrics

    Returns:
        TripCheckResponse with prediction results

    Raises:
        HTTPException: If validation fails
    """
    try:
        result = predictor.predict_trip_safety(
            trip_distance_km=data.trip_distance_km,
            km_since_last_oil_change=data.km_since_last_oil_change,
            engine_temp_celsius=data.engine_temp_celsius,
            oil_level_percent=data.oil_level_percent,
            passenger_load_percent=data.passenger_load_percent,
        )

        response = TripCheckResponse(
            status=result["status"],
            trip_distance_km=result["trip_distance_km"],
            remaining_autonomy_km=result["remaining_autonomy_km"],
            predicted_breakdown_km=result.get("predicted_breakdown_km"),
            critical_location=result.get("critical_location"),
            recommendation=result["recommendation"],
            message=result["message"],
            safety_margin_km=result["safety_margin_km"],
        )
        return response

    except ValueError as exc:
        logger.warning(f"Validation error in predict_trip: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(exc), "message": "Les données du trajet sont invalides."},
        ) from exc
    except Exception as exc:
        logger.error(f"Unexpected error in predict_trip: {exc}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal server error",
                "message": "Une erreur interne s'est produite. Veuillez réessayer plus tard.",
            },
        ) from exc
