def predict_trip_safety(
    trip_distance_km: int,
    km_since_last_oil_change: int,
    engine_temp_celsius: float,
    oil_level_percent: float,
    passenger_load_percent: float,
) -> dict:
    """Evaluate the safety of a trip based on oil wear, temperature, and load.

    Returns a normalized response payload used by the FastAPI layer.
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

    max_oil_lifespan_km = 5000.0

    if engine_temp_celsius > 100:
        temp_factor = 2.0
    elif engine_temp_celsius > 92:
        temp_factor = 1.3
    else:
        temp_factor = 1.0

    load_factor = 1.0 + (passenger_load_percent / 100.0) * 0.3
    remaining_oil_km = (max_oil_lifespan_km - km_since_last_oil_change) / (temp_factor * load_factor)

    if oil_level_percent < 30:
        remaining_oil_km *= (oil_level_percent / 100.0)

    remaining_oil_km = max(0.0, remaining_oil_km)
    margin_km = remaining_oil_km - trip_distance_km
    predicted_breakdown_km = round(remaining_oil_km)

    critical_location = None
    if 160 <= predicted_breakdown_km <= 200:
        critical_location = "Aux alentours de Toumodi (KM 185)"
    elif predicted_breakdown_km < 160:
        critical_location = "Entre Abidjan et Singrobo"
    elif 200 < predicted_breakdown_km < trip_distance_km:
        critical_location = "Entre Toumodi et Yamoussoukro"

    if margin_km < 0:
        status = "CRITICAL_RISK"
        recommendation = "Vidange moteur urgente et vérification du liquide de refroidissement avant départ."
        message = "Le véhicule présente un risque élevé avant le départ; une intervention urgente est recommandée."
    elif margin_km < 50:
        status = "WARNING"
        recommendation = "Trajet possible, prévoir révision dès l'arrivée."
        message = "Le véhicule est viable pour le trajet, mais une maintenance préventive est recommandée."
    else:
        status = "SAFE"
        recommendation = "Véhicule prêt pour le trajet."
        message = "Le véhicule est en bonne condition pour effectuer ce trajet."

    return {
        "status": status,
        "trip_distance_km": trip_distance_km,
        "remaining_autonomy_km": round(remaining_oil_km),
        "predicted_breakdown_km": predicted_breakdown_km if margin_km < 0 else None,
        "critical_location": critical_location if margin_km < 0 else None,
        "recommendation": recommendation,
        "message": message,
    }
