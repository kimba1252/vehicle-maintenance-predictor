# vehicle-maintenance-predictor
Application de maintenance prédictive et suivi de télémétrie pour les flottes de transport en Côte d'Ivoire (Abidjan - Yamoussoukro).

## Fonctionnalités
- Détection des pannes avant le départ : analyse de la température moteur, de la charge et de l'usure de l'huile.
- Géolocalisation du point de rupture : estimation de la zone d'arrêt du véhicule (Toumodi, Singrobo, Yamoussoukro).
- API REST via FastAPI pour intégrer la prédiction dans des outils de gestion de flotte.

## Prérequis
- Python 3.10+
- pip
- Un environnement virtuel recommandé

## Installation
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Variables d'environnement
Copier le fichier `.env.example` et remplir les valeurs
```bash
cp .env.example .env
```

## Démarrage de l'API
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints principaux
- `GET /` : vérification de disponibilité
- `GET /health` : santé du service
- `POST /predict-trip` : prédiction d'un trajet

## Exemple de payload
```json
{
  "trip_distance_km": 240,
  "km_since_last_oil_change": 4200,
  "engine_temp_celsius": 96,
  "oil_level_percent": 65,
  "passenger_load_percent": 80
}
```

## Exemple de réponse
```json
{
  "status": "WARNING",
  "trip_distance_km": 240,
  "remaining_autonomy_km": 170,
  "predicted_breakdown_km": null,
  "critical_location": null,
  "recommendation": "Trajet possible, prévoir révision dès l'arrivée.",
  "message": "Le véhicule est viable pour le trajet, mais une maintenance préventive est recommandée."
}
```

## Tests
```bash
pytest
```
