"""Database service for Supabase integration."""

import logging
from typing import Optional

from backend.config import settings

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for managing database operations with Supabase."""

    def __init__(self):
        """Initialize database service."""
        self.enabled = settings.supabase_enabled
        self.client = None

        if self.enabled:
            self._initialize_supabase()

    def _initialize_supabase(self) -> None:
        """Initialize Supabase client if credentials are available."""
        if not settings.supabase_url or not settings.supabase_key:
            logger.warning(
                "Supabase is enabled but URL or KEY are not configured. "
                "Database operations will be skipped."
            )
            self.enabled = False
            return

        try:
            from supabase import create_client

            self.client = create_client(settings.supabase_url, settings.supabase_key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            self.enabled = False

    def save_trip_prediction(
        self,
        vehicle_id: str,
        destination: str,
        distance_km: int,
        prediction_result: dict,
    ) -> Optional[dict]:
        """Save trip prediction result to database.

        Args:
            vehicle_id: Vehicle identifier
            destination: Trip destination
            distance_km: Trip distance in kilometers
            prediction_result: Prediction result from predictor

        Returns:
            Server response or None if database is disabled
        """
        if not self.enabled or not self.client:
            logger.debug("Database is disabled. Skipping prediction save.")
            return None

        try:
            data = {
                "vehicle_id": vehicle_id,
                "departure_city": "Abidjan",
                "destination_city": destination,
                "trip_distance_km": distance_km,
                "status": prediction_result["status"],
                "predicted_breakdown_km": prediction_result.get("predicted_breakdown_km"),
                "critical_location": prediction_result.get("critical_location"),
                "recommendation": prediction_result["recommendation"],
            }

            response = self.client.table("trip_predictions").insert(data).execute()
            logger.info(f"Trip prediction saved successfully for vehicle {vehicle_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to save trip prediction: {e}")
            return None


# Global database instance
database = DatabaseService()
