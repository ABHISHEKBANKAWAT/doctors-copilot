import logging
from typing import List, Dict, Any, Optional
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
from src.config.bigquery_config import bq_config

# Configure logging
logger = logging.getLogger(__name__)

# Constants
DEFAULT_LIMIT = 1000
MIMIC_DATASET = 'mimic3_clinical'

def execute_bigquery_query(client: bigquery.Client, query: str, params: Optional[List] = None) -> bigquery.QueryJob:
    """Execute a BigQuery query with error handling and logging."""
    try:
        job_config = bigquery.QueryJobConfig()
        if params:
            job_config.query_parameters = params
            
        logger.info(f"Executing BigQuery query: {query[:200]}...")
        query_job = client.query(query, job_config=job_config)
        return query_job
        
    except Exception as e:
        logger.error(f"Error executing BigQuery query: {str(e)}")
        raise

def get_patient_insights(limit: int = DEFAULT_LIMIT) -> List[Dict[str, Any]]:
    """
    Retrieve patient insights from BigQuery with optimized query.
    
    Args:
        limit: Maximum number of results to return
        
    Returns:
        List of patient insights
    """
    client = bq_config.get_client()
    
    # Define the query with parameterized values
    query = f"""
    WITH latest_notes AS (
      SELECT 
        hadm_id,
        text,
        ROW_NUMBER() OVER(PARTITION BY hadm_id ORDER BY chartdate DESC, charttime DESC) as rn
      FROM `{MIMIC_DATASET}.noteevents`
      WHERE text IS NOT NULL
    ),
    aggregated_vitals AS (
      SELECT
        hadm_id,
        AVG(CASE WHEN itemid IN (220045, 220050) THEN valuenum ELSE NULL END) as heart_rate,
        AVG(CASE WHEN itemid = 220050 THEN valuenum ELSE NULL END) as systolic_bp,
        AVG(CASE WHEN itemid = 220051 THEN valuenum ELSE NULL END) as diastolic_bp
      FROM `{MIMIC_DATASET}.chartevents`
      WHERE itemid IN (220045, 220050, 220051)  -- Heart Rate, NBP, NBP
      GROUP BY hadm_id
    ),
    latest_labs AS (
      SELECT
        hadm_id,
        AVG(CASE WHEN itemid = 50931 THEN valuenum ELSE NULL END) as glucose,
        AVG(CASE WHEN itemid = 50912 THEN valuenum ELSE NULL END) as creatinine
      FROM `{MIMIC_DATASET}.labevents`
      WHERE itemid IN (50931, 50912)  -- Glucose, Creatinine
      GROUP BY hadm_id
    )
    SELECT
      p.subject_id as patient_id,
      p.hadm_id,
      p.admittime,
      p.dischtime,
      p.deathtime,
      p.admission_type,
      p.diagnosis,
      p.hospital_expire_flag,
      v.heart_rate,
      v.systolic_bp,
      v.diastolic_bp,
      l.glucose,
      l.creatinine,
      n.text as clinical_notes,
      -- Calculate risk score based on vitals and labs
      CASE
        WHEN v.systolic_bp < 90 OR v.diastolic_bp < 60 THEN 80  -- Hypotension
        WHEN v.heart_rate > 100 THEN 70  -- Tachycardia
        WHEN l.glucose > 180 THEN 65  -- Hyperglycemia
        WHEN l.creatinine > 1.3 THEN 60  -- Elevated creatinine
        ELSE 30  -- Low risk
      END as risk_score,
      -- Generate clinical insights
      TO_JSON_STRING(ARRAY(
        SELECT AS STRUCT 
          'vital_signs' as category,
          'Vital Signs' as title,
          TO_JSON_STRING(STRUCT(
            v.heart_rate as heart_rate,
            v.systolic_bp as systolic_bp,
            v.diastolic_bp as diastolic_bp
          )) as data
        WHERE v.hadm_id IS NOT NULL
        
        UNION ALL
        
        SELECT
          'lab_results' as category,
          'Lab Results' as title,
          TO_JSON_STRING(STRUCT(
            l.glucose as glucose,
            l.creatinine as creatinine
          )) as data
        WHERE l.hadm_id IS NOT NULL
      )) as insights_json
    FROM `{MIMIC_DATASET}.admissions` p
    LEFT JOIN aggregated_vitals v ON p.hadm_id = v.hadm_id
    LEFT JOIN latest_labs l ON p.hadm_id = l.hadm_id
    LEFT JOIN latest_notes n ON p.hadm_id = n.hadm_id AND n.rn = 1
    WHERE p.hadm_id IS NOT NULL
      AND p.admittime >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 YEAR)
    ORDER BY p.admittime DESC
    LIMIT @limit
    """
    
    # Execute the query with parameters
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("limit", "INT64", limit)
        ]
    )
    
    try:
        query_job = client.query(query, job_config=job_config)
        results = list(query_job.result())
        logger.info(f"Retrieved {len(results)} patient records from BigQuery")
        return results
        
    except GoogleAPIError as e:
        logger.error(f"Google BigQuery API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_patient_insights: {str(e)}")
        raise

def format_insights(results: List[Any]) -> List[Dict[str, Any]]:
    """
    Format the raw query results into a more usable structure.
    
    Args:
        results: List of BigQuery Row objects
        
    Returns:
        List of formatted patient insights
    """
    formatted_results = []
    
    for row in results:
        try:
            # Parse the insights JSON if available
            insights = []
            if hasattr(row, 'insights_json') and row.insights_json:
                try:
                    insights = eval(row.insights_json) if row.insights_json else []
                except Exception as e:
                    logger.warning(f"Error parsing insights JSON: {str(e)}")
            
            # Create the patient assessment
            assessment = {
                'concern_level': 'High' if row.risk_score >= 70 else 
                               'Medium' if row.risk_score >= 40 else 'Low',
                'key_findings': [],
                'recommendations': []
            }
            
            # Add findings based on risk factors
            if getattr(row, 'systolic_bp', 0) < 90 or getattr(row, 'diastolic_bp', 0) < 60:
                assessment['key_findings'].append('Hypotension detected')
                assessment['recommendations'].append('Monitor blood pressure closely')
                
            if getattr(row, 'glucose', 0) > 180:
                assessment['key_findings'].append('Hyperglycemia detected')
                assessment['recommendations'].append('Monitor blood glucose levels')
            
            # Add the formatted result
            formatted_results.append({
                'patient_id': getattr(row, 'patient_id', 'N/A'),
                'admission_id': getattr(row, 'hadm_id', 'N/A'),
                'admission_date': getattr(row, 'admittime', None).isoformat() if hasattr(row, 'admittime') and row.admittime else None,
                'discharge_date': getattr(row, 'dischtime', None).isoformat() if hasattr(row, 'dischtime') and row.dischtime else None,
                'admission_type': getattr(row, 'admission_type', 'Unknown'),
                'diagnosis': getattr(row, 'diagnosis', 'Not specified'),
                'vital_signs': {
                    'heart_rate': round(getattr(row, 'heart_rate', 0), 2) if hasattr(row, 'heart_rate') and row.heart_rate is not None else None,
                    'systolic_bp': round(getattr(row, 'systolic_bp', 0)) if hasattr(row, 'systolic_bp') and row.systolic_bp is not None else None,
                    'diastolic_bp': round(getattr(row, 'diastolic_bp', 0)) if hasattr(row, 'diastolic_bp') and row.diastolic_bp is not None else None,
                },
                'lab_results': {
                    'glucose': round(getattr(row, 'glucose', 0), 2) if hasattr(row, 'glucose') and row.glucose is not None else None,
                    'creatinine': round(getattr(row, 'creatinine', 0), 2) if hasattr(row, 'creatinine') and row.creatinine is not None else None,
                },
                'risk_score': int(getattr(row, 'risk_score', 0)) if hasattr(row, 'risk_score') and row.risk_score is not None else 0,
                'clinical_insights': getattr(row, 'clinical_notes', 'No clinical notes available'),
                'patient_assessment': assessment,
                'insights': insights
            })
            
        except Exception as e:
            logger.error(f"Error formatting row: {str(e)}")
            continue
    
    return formatted_results
