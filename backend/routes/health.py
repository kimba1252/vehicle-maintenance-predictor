"""Health check routes."""

from fastapi import APIRouter

from backend.config import settings
from backend.models import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=dict, tags=["root"])
def root():
    """Root endpoint."""
    return {
        "status": "online",
        "message": "API de Maintenance Prédictive Opérationnelle",
        "version": settings.api_version,
        "environment": settings.env,
    }


@router.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        service="vehicle-maintenance-predictor",
        version=settings.api_version,
    )
