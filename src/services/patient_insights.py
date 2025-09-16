from src.config.bigquery_config import bq_config

def get_patient_insights():
    client = bq_config.get_client()
    query = """
    -- Core Patient Insights Query: Multimodal Analysis with BigQuery ML/AI
WITH patient_multimodal AS (
  SELECT
    p.subject_id AS patient_id,                       -- MIMIC-III: unique patient identifier
    p.admittime,                                      -- Admission time
    p.gender,                                         -- Gender from demographic table
    p.age,                                            -- Age from demographic table
    p.diagnosis,                                      -- Primary diagnosis (if available)
    p.hadm_id,                                        -- Hospital admission ID
    -- Example: Structured vitals and lab data (replace/add columns for full context)
    v.heart_rate, v.systolic_bp, v.diastolic_bp,      -- Vitals from chart_events table
    l.glucose, l.creatinine,                          -- Labs from lab_events table

    -- Structured risk score estimation (example using AI.GENERATE_DOUBLE)
    AI.GENERATE_DOUBLE(
      CONCAT(
        'Risk score 0-100 for patient: age ', CAST(p.age AS STRING), 
        ', gender: ', p.gender,
        ', diagnosis: ', p.diagnosis,
        ', vitals: HR ', CAST(v.heart_rate AS STRING), 
        ', BP ', CAST(v.systolic_bp AS STRING), '/', CAST(v.diastolic_bp AS STRING), 
        ', glucose ', CAST(l.glucose AS STRING)
      )
    ) AS risk_score,

    -- Key medical insights extracted from clinical notes (unstructured text)
    AI.GENERATE_TEXT(
      CONCAT(
        'Analyze this clinical note and extract key medical insights: ',
        n.text
      )
    ) AS clinical_insights,

    -- Generate structured patient assessment table
    AI.GENERATE_TABLE(
      CONCAT('Create assessment table for patient with vitals (HR:', CAST(v.heart_rate AS STRING), 
        ', BP:', CAST(v.systolic_bp AS STRING), '/', CAST(v.diastolic_bp AS STRING), 
        ') and labs (glucose:', CAST(l.glucose AS STRING), ', creatinine:', CAST(l.creatinine AS STRING), ')'),
      STRUCT<
        concern_level STRING,
        key_findings STRING,
        immediate_actions STRING,
        monitoring_needed STRING
      >
    ) AS patient_assessment

  FROM
    `bigquery-public-data.mimic3_clinical.admissions` p
  LEFT JOIN
    `bigquery-public-data.mimic3_clinical.chart_events` v
    ON p.hadm_id = v.hadm_id
  LEFT JOIN
    `bigquery-public-data.mimic3_clinical.lab_events` l
    ON p.hadm_id = l.hadm_id
  LEFT JOIN
    `bigquery-public-data.mimic3_clinical.noteevents` n
    ON p.hadm_id = n.hadm_id
  WHERE
    p.age >= 18 -- Example filter: adults only
    AND n.text IS NOT NULL -- Include only patients with clinical notes
    -- Additional filters as appropriate for your use case
)
SELECT * FROM patient_multimodal
LIMIT 100;

    """
    job = client.query(query)
    return job.result()

    
def format_insights(results):
    insights = []
    for row in results:
        insights.append({
            "patient_id": row.patient_id,
            "risk_score": row.risk_score,
            "clinical_insights": row.clinical_insights,
            "patient_assessment": row.patient_assessment
        })
    return insights
