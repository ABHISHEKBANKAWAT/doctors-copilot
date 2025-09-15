import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT")
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    BIGQUERY_DATASET: str = os.getenv("BIGQUERY_DATASET", "healthcare_copilot")
    BIGQUERY_LOCATION: str = os.getenv("BIGQUERY_LOCATION", "US")
    
    class Config:
        env_file = ".env"

settings = Settings()
