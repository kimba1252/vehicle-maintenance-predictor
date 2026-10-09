def predict_trip_safety(
    trip_distance_km: int, 
    km_since_last_oil_change: int, 
    engine_temp_celsius: float, 
    oil_level_percent: float, 
    passenger_load_percent: float
) -> dict:
    MAX_OIL_LIFESPAN_KM = 5000
    
    # Facteur d'usure selon la température
    if engine_temp_celsius > 100:
        temp_factor = 2.0
    elif engine_temp_celsius > 92:
        temp_factor = 1.3
    else:
        temp_factor = 1.0

    # Facteur d'usure selon la charge
    load_factor = 1.0 + (passenger_load_percent / 100.0) * 0.3

    # Calcul autonomie restante
    remaining_oil_km = (MAX_OIL_LIFESPAN_KM - km_since_last_oil_change) / (temp_factor * load_factor)
    
    if oil_level_percent < 30:
        remaining_oil_km *= (oil_level_percent / 100.0)

    margin_km = remaining_oil_km - trip_distance_km
    predicted_breakdown_km = round(remaining_oil_km)

    # Localisation axe Abidjan - Yamoussoukro (240 km)
    critical_location = "Aucune"
    if 160 <= predicted_breakdown_km <= 200:
        critical_location = "Aux alentours de Toumodi (KM 185)"
    elif predicted_breakdown_km < 160:
        critical_location = "Entre Abidjan et Singrobo"
    elif 200 < predicted_breakdown_km < trip_distance_km:
        critical_location = "Entre Toumodi et Yamoussoukro"

    if margin_km < 0:
        status = "CRITICAL_RISK"
        recommendation = "Vidange moteur urgente et vérification du liquide de refroidissement avant départ."
    elif margin_km < 50:
        status = "WARNING"
        recommendation = "Trajet possible, prévoir révision dès l'arrivée."
    else:
        status = "SAFE"
        recommendation = "Véhicule prêt pour le trajet."

    return {
        "status": status,
        "trip_distance_km": trip_distance_km,
        "remaining_autonomy_km": round(remaining_oil_km),
        "predicted_breakdown_km": predicted_breakdown_km if margin_km < 0 else None,
        "critical_location": critical_location if margin_km < 0 else None,
        "recommendation": recommendation
    }
