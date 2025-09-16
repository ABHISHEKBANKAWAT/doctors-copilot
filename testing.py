from src.services import bigquery_service

query = """
SELECT
  *
FROM
  ML.GENERATE_TEXT(
    MODEL `doctors-copilot-2025.your_llm_model_name`,
    (SELECT 'Summarize this clinical note: ...' AS prompt),
    STRUCT(
      1024 AS max_output_tokens,
      0.2 AS temperature,
      0.8 AS top_p
    )
  )
"""
results_df = bigquery_service.bq_service.execute_query(query)
print(results_df)
