"""Prediction service for vehicle maintenance risk assessment."""

from backend.config import settings
from backend.constants import BREAKDOWN_ZONES, TEMP_WEAR_FACTORS, TripStatus


class PredictionService:
    """Service for predicting trip safety based on vehicle metrics."""

    def __init__(
        self,
        max_oil_lifespan_km: int = settings.max_oil_lifespan_km,
        warning_margin_km: int = settings.warning_margin_km,
    ):
        """Initialize prediction service with configurable parameters.

        Args:
            max_oil_lifespan_km: Maximum oil lifespan in kilometers
            warning_margin_km: Margin for warning status in kilometers
        """
        self.max_oil_lifespan_km = max_oil_lifespan_km
        self.warning_margin_km = warning_margin_km

    def predict_trip_safety(
        self,
        trip_distance_km: int,
        km_since_last_oil_change: int,
        engine_temp_celsius: float,
        oil_level_percent: float,
        passenger_load_percent: float,
    ) -> dict:
        """Evaluate the safety of a trip based on vehicle metrics.

        Args:
            trip_distance_km: Planned trip distance
            km_since_last_oil_change: Kilometers since last oil change
            engine_temp_celsius: Current engine temperature
            oil_level_percent: Current oil level percentage
            passenger_load_percent: Passenger load percentage

        Returns:
            Dictionary with prediction results

        Raises:
            ValueError: If any input value is invalid
        """
        self._validate_inputs(
            trip_distance_km,
            km_since_last_oil_change,
            engine_temp_celsius,
            oil_level_percent,
            passenger_load_percent,
        )

        # Calculate wear factors
        temp_factor = self._calculate_temp_factor(engine_temp_celsius)
        load_factor = self._calculate_load_factor(passenger_load_percent)

        # Calculate remaining oil autonomy
        remaining_oil_km = self._calculate_remaining_autonomy(
            km_since_last_oil_change, temp_factor, load_factor, oil_level_percent
        )

        # Calculate safety margin
        safety_margin_km = remaining_oil_km - trip_distance_km
        predicted_breakdown_km = round(remaining_oil_km)

        # Determine trip status and recommendations
        status, recommendation, message = self._determine_status(
            safety_margin_km, temp_factor, oil_level_percent, km_since_last_oil_change
        )

        # Determine critical location if risk exists
        critical_location = None
        if status == TripStatus.CRITICAL_RISK:
            critical_location = self._determine_location(predicted_breakdown_km, trip_distance_km)

        return {
            "status": status,
            "trip_distance_km": trip_distance_km,
            "remaining_autonomy_km": round(remaining_oil_km),
            "predicted_breakdown_km": predicted_breakdown_km if safety_margin_km < 0 else None,
            "critical_location": critical_location,
            "recommendation": recommendation,
            "message": message,
            "safety_margin_km": round(safety_margin_km, 1),
        }

    def _validate_inputs(
        self,
        trip_distance_km: int,
        km_since_last_oil_change: int,
        engine_temp_celsius: float,
        oil_level_percent: float,
        passenger_load_percent: float,
    ) -> None:
        """Validate all input parameters.

        Raises:
            ValueError: If any input is invalid
        """
        if trip_distance_km <= 0:
            raise ValueError("trip_distance_km must be greater than 0.")
        if km_since_last_oil_change < 0:
            raise ValueError("km_since_last_oil_change must be greater than or equal to 0.")
        if engine_temp_celsius < 0:
            raise ValueError("engine_temp_celsius must be greater than or equal to 0.")
        if not 0 <= oil_level_percent <= 100:
            raise ValueError("oil_level_percent must be between 0 and 100.")
        if not 0 <= passenger_load_percent <= 100:
            raise ValueError("passenger_load_percent must be between 0 and 100.")

    def _calculate_temp_factor(self, temp_celsius: float) -> float:
        """Calculate wear factor based on engine temperature.

        Args:
            temp_celsius: Engine temperature in Celsius

        Returns:
            Temperature wear factor
        """
        if temp_celsius > 100:
            return TEMP_WEAR_FACTORS["hot"]
        elif temp_celsius > 92:
            return TEMP_WEAR_FACTORS["warm"]
        else:
            return TEMP_WEAR_FACTORS["normal"]

    def _calculate_load_factor(self, load_percent: float) -> float:
        """Calculate wear factor based on passenger load.

        Args:
            load_percent: Passenger load percentage

        Returns:
            Load wear factor
        """
        return 1.0 + (load_percent / 100.0) * 0.3

    def _calculate_remaining_autonomy(
        self,
        km_since_oil_change: int,
        temp_factor: float,
        load_factor: float,
        oil_level_percent: float,
    ) -> float:
        """Calculate remaining oil autonomy in kilometers.

        Args:
            km_since_oil_change: Kilometers since last oil change
            temp_factor: Temperature wear factor
            load_factor: Load wear factor
            oil_level_percent: Current oil level percentage

        Returns:
            Remaining autonomy in kilometers
        """
        remaining_km = (self.max_oil_lifespan_km - km_since_oil_change) / (
            temp_factor * load_factor
        )

        # Reduce autonomy if oil level is low
        if oil_level_percent < 30:
            remaining_km *= oil_level_percent / 100.0

        return max(0.0, remaining_km)

    def _determine_status(
        self,
        safety_margin_km: float,
        temp_factor: float,
        oil_level_percent: float,
        km_since_oil_change: int,
    ) -> tuple[str, str, str]:
        """Determine trip status and generate recommendations.

        Args:
            safety_margin_km: Safety margin in kilometers
            temp_factor: Temperature wear factor
            oil_level_percent: Current oil level percentage
            km_since_oil_change: Kilometers since last oil change

        Returns:
            Tuple of (status, recommendation, message)
        """
        if safety_margin_km < 0:
            recommendation_parts = []
            if oil_level_percent < 50:
                recommendation_parts.append("Faire l'appoint d'huile moteur immédiatement.")
            if km_since_oil_change > 4000:
                recommendation_parts.append("Effectuer la vidange moteur complète.")
            if temp_factor > 1.3:
                recommendation_parts.append(
                    "Vérifier le liquide de refroidissement et le radiateur."
                )

            if not recommendation_parts:
                recommendation = "Inspection complète du moteur requise avant le départ."
            else:
                recommendation = " ".join(recommendation_parts)

            return (
                TripStatus.CRITICAL_RISK,
                recommendation,
                "Le véhicule présente un risque élevé avant le départ; une intervention urgente est recommandée.",
            )

        elif safety_margin_km < self.warning_margin_km:
            return (
                TripStatus.WARNING,
                "Trajet possible, prévoir révision dès l'arrivée.",
                "Le véhicule est viable pour le trajet, mais une maintenance préventive est recommandée.",
            )

        else:
            return (
                TripStatus.SAFE,
                "Véhicule prêt pour le trajet.",
                "Le véhicule est en bonne condition pour effectuer ce trajet.",
            )

    def _determine_location(self, predicted_breakdown_km: int, trip_distance_km: int) -> str:
        """Determine the likely breakdown location on the route.

        Args:
            predicted_breakdown_km: Predicted breakdown distance
            trip_distance_km: Total trip distance

        Returns:
            Description of the breakdown zone
        """
        if predicted_breakdown_km > trip_distance_km:
            return "Hors de la zone couverte"

        for zone in BREAKDOWN_ZONES:
            if zone["min_km"] <= predicted_breakdown_km <= zone["max_km"]:
                return zone["zone"]

        return "Zone indéterminée"


# Global predictor instance
predictor = PredictionService()
