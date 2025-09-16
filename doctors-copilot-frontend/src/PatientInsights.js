import React, { useEffect, useState } from 'react';

const PatientInsights = () => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/patient_insights') // adjust to your backend endpoint
      .then(response => response.json())
      .then(data => {
        setInsights(data);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Patient Insights</h2>
      {insights.map((item, idx) => (
        <div key={idx} style={{border: "1px solid #ccc", padding: 16, marginBottom: 16}}>
          <div><strong>Patient ID:</strong> {item.patient_id}</div>
          <div><strong>Risk Score:</strong> {item.risk_score}</div>
          <div><strong>Clinical Insights:</strong> {item.clinical_insights}</div>
          <div>
            <strong>Assessment:</strong>
            <pre>{JSON.stringify(item.patient_assessment, null, 2)}</pre>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PatientInsights;
