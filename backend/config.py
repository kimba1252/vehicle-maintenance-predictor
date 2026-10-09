"""Configuration module for environment and settings."""

import os
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # API Settings
    api_title: str = "Vehicle Maintenance Predictor API"
    api_version: str = "2.0.0"
    api_description: str = (
        "API de maintenance prédictive pour flottes de transport "
        "et suivi de santé du véhicule en Côte d'Ivoire."
    )
    api_host: str = Field(default="0.0.0.0", validation_alias="API_HOST")
    api_port: int = Field(default=8000, validation_alias="API_PORT")
    debug: bool = Field(default=False, validation_alias="DEBUG")

    # Database Settings
    supabase_url: str = Field(default="", validation_alias="SUPABASE_URL")
    supabase_key: str = Field(default="", validation_alias="SUPABASE_KEY")
    supabase_enabled: bool = Field(default=False, validation_alias="SUPABASE_ENABLED")

    # Prediction Settings
    max_oil_lifespan_km: int = Field(default=5000, validation_alias="MAX_OIL_LIFESPAN_KM")
    warning_margin_km: int = Field(default=50, validation_alias="WARNING_MARGIN_KM")

    # Environment
    env: Literal["development", "staging", "production"] = Field(
        default="development", validation_alias="ENVIRONMENT"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
