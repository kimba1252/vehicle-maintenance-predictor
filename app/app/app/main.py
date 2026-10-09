from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.predictor import analyser_sante_trajet
from app.database import enregistrer_prediction

app = FastAPI(
    title="API de Maintenance Prédictive de Trajet",
    description="API pour prédire l'état de santé des véhicules de transport sur les axes routiers en Côte d'Ivoire."
)

class TripPredictionRequest(BaseModel):
    vehicle_id: str
    destination_city: str = "Yamoussoukro"
    distance_trajet_km: float = 240.0
    km_depuis_vidange: int
    temp_moteur_celsius: float
    niveau_huile_percent: float
    charge_passagers_percent: float

@app.get("/")
def home():
    return {"status": "Online", "system": "Predictive Vehicle Maintenance API"}

@app.post("/predict")
def predict_trip_health(payload: TripPredictionRequest):
    try:
        # 1. Calcul de la prédiction
        resultats = analyser_sante_trajet(
            distance_trajet_km=payload.distance_trajet_km,
            km_depuis_vidange=payload.km_depuis_vidange,
            temp_moteur_celsius=payload.temp_moteur_celsius,
            niveau_huile_percent=payload.niveau_huile_percent,
            charge_passagers_percent=payload.charge_passagers_percent
        )
        
        # 2. Enregistrement dans la base de données Supabase
        enregistrer_prediction(
            vehicle_id=payload.vehicle_id,
            destination=payload.destination_city,
            distance_km=int(payload.distance_trajet_km),
            resultats=resultats
        )
        
        return {
            "vehicle_id": payload.vehicle_id,
            "trajet": f"Abidjan -> {payload.destination_city}",
            "prediction": resultats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
