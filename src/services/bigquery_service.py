from google.cloud import bigquery
from src.config.bigquery_config import bq_config
import pandas as pd
from src.config.settings import settings

class BigQueryService:
    def __init__(self):
        self.client = bq_config.get_client()
        self.dataset_id = bq_config.get_dataset_id()
        self.location = settings.BIGQUERY_LOCATION

    def execute_query(self, query: str):
        job = self.client.query(query, location=self.location)
        result = job.result()
        return result.to_dataframe()
    
    def insert_rows(self, table_name, rows):
        table_ref = f"{self.dataset_id}.{table_name}"
        table = self.client.get_table(table_ref)
        errors = self.client.insert_rows_json(table, rows)
        return len(errors) == 0

bq_service = BigQueryService()  
