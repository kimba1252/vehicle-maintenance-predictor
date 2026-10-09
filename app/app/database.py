import os
from supabase import create_client, Client

# Remplace par les clés d'accès de ton projet Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://TON_PROJET.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "TA_CLE_ANON_SUPABASE")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def enregistrer_prediction(vehicle_id: str, destination: str, distance_km: int, resultats: dict):
    """
    Sauvegarde le résultat de la prédiction dans la table `trip_predictions` sur Supabase.
    """
    data = {
        "vehicle_id": vehicle_id,
        "departure_city": "Abidjan",
        "destination_city": destination,
        "trip_distance_km": distance_km,
        "status": resultats["status"],
        "predicted_breakdown_km": resultats["point_rupture_km"],
        "recommended_actions": " | ".join(resultats["actions_recommandees"])
    }
    
    response = supabase.table("trip_predictions").insert(data).execute()
    return response
