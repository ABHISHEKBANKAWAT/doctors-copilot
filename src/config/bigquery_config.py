from google.cloud import bigquery
from google.oauth2 import service_account
from src.config.settings import settings


class BigQueryConfig:
    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_APPLICATION_CREDENTIALS
        )
        self.client = bigquery.Client(
            credentials=credentials, project=settings.GOOGLE_CLOUD_PROJECT
        )
        self.dataset_id = f"{settings.GOOGLE_CLOUD_PROJECT}.{settings.BIGQUERY_DATASET}"

    def get_client(self):
        return self.client

    def get_dataset_id(self):
        return self.dataset_id

bq_config = BigQueryConfig()
