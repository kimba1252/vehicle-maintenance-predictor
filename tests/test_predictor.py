import pytest

from backend.predictor import predict_trip_safety


def test_predict_trip_safe_case():
    result = predict_trip_safety(
        trip_distance_km=240,
        km_since_last_oil_change=1000,
        engine_temp_celsius=88,
        oil_level_percent=70,
        passenger_load_percent=20,
    )

    assert result["status"] in {"SAFE", "WARNING", "CRITICAL_RISK"}
    assert result["trip_distance_km"] == 240
    assert "message" in result
    assert "recommendation" in result


def test_predict_trip_warning_case():
    result = predict_trip_safety(
        trip_distance_km=240,
        km_since_last_oil_change=4500,
        engine_temp_celsius=95,
        oil_level_percent=50,
        passenger_load_percent=60,
    )

    assert result["status"] in {"WARNING", "CRITICAL_RISK"}


def test_predict_trip_invalid_inputs():
    with pytest.raises(ValueError):
        predict_trip_safety(
            trip_distance_km=0,
            km_since_last_oil_change=2000,
            engine_temp_celsius=90,
            oil_level_percent=60,
            passenger_load_percent=20,
        )

    with pytest.raises(ValueError):
        predict_trip_safety(
            trip_distance_km=240,
            km_since_last_oil_change=3000,
            engine_temp_celsius=90,
            oil_level_percent=120,
            passenger_load_percent=20,
        )
