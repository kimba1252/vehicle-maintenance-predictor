import math

def analyser_sante_trajet(
    distance_trajet_km: float, 
    km_depuis_vidange: int, 
    temp_moteur_celsius: float, 
    niveau_huile_percent: float, 
    charge_passagers_percent: float
):
    """
    Calcule la marge de sécurité et localise le point de rupture prédictif.
    """
    LIFESPAN_HUILE_KM = 5000 
    
    # Facteur d'usure selon la température
    if temp_moteur_celsius > 100:
        facteur_temp = 2.0
    elif temp_moteur_celsius > 92:
        facteur_temp = 1.3
    else:
        facteur_temp = 1.0
        
    # Facteur d'usure selon la charge du véhicule
    facteur_charge = 1.0 + (charge_passagers_percent / 100.0) * 0.3

    # Autonomie restante en kilomètres
    km_restants_huile = (LIFESPAN_HUILE_KM - km_depuis_vidange) / (facteur_temp * facteur_charge)
    
    if niveau_huile_percent < 30:
        km_restants_huile *= (niveau_huile_percent / 100.0)

    km_depuis_abidjan = round(km_restants_huile)
    marge_securite_km = km_restants_huile - distance_trajet_km

    # Analyse de la zone de panne sur l'axe Abidjan - Yamoussoukro (240 km)
    zone_panne = None
    status = "SAFE"
    actions = []

    if marge_securite_km < 0:
        status = "CRITICAL_RISK"
        if 160 <= km_depuis_abidjan <= 200:
            zone_panne = "Toumodi (KM 185-190)"
        elif km_depuis_abidjan < 160:
            zone_panne = "Entre Abidjan et Singrobo (KM 100-140)"
        else:
            zone_panne = "Entre Toumodi et Yamoussoukro (KM 210-230)"
            
        if niveau_huile_percent < 50:
            actions.append("Faire l'appoint d'huile moteur immédiatement.")
        if km_depuis_vidange > 4000:
            actions.append("Effectuer la vidange moteur complète.")
        if temp_moteur_celsius > 95:
            actions.append("Vérifier le liquide de refroidissement et le radiateur.")
            
    elif marge_securite_km < 50:
        status = "WARNING"
        actions.append("Révision recommandée à la fin de ce trajet.")

    return {
        "status": status,
        "marge_securite_km": round(marge_securite_km, 1),
        "autonomie_estimee_km": round(km_restants_huile, 1),
        "point_rupture_km": km_depuis_abidjan if status == "CRITICAL_RISK" else None,
        "zone_panne_estimee": zone_panne,
        "actions_recommandees": actions
    }
