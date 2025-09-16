import React, { useEffect, useState, useCallback } from 'react';
import { Card, Spin, Alert, Button, Typography, Divider, Space } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import './PatientInsights.css';

const { Title, Text } = Typography;

const PatientInsights = () => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchInsights = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('http://localhost:5000/api/patient_insights');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setInsights(data);
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Error fetching insights:', err);
      setError(`Failed to load patient insights: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchInsights();
  }, [fetchInsights]);

  const handleRefresh = () => {
    fetchInsights();
  };

  const renderRiskBadge = (score) => {
    if (score >= 75) return <span className="risk-badge high">High Risk</span>;
    if (score >= 50) return <span className="risk-badge medium">Medium Risk</span>;
    return <span className="risk-badge low">Low Risk</span>;
  };

  if (loading && insights.length === 0) {
    return (
      <div className="loading-container">
        <Spin size="large" />
        <p>Loading patient insights...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error"
        description={error}
        type="error"
        action={
          <Button size="small" danger onClick={fetchInsights}>
            Retry
          </Button>
        }
      />
    );
  }

  return (
    <div className="patient-insights-container">
      <div className="header-section">
        <Title level={2}>Patient Insights</Title>
        <div className="controls">
          <Button 
            type="primary" 
            icon={<ReloadOutlined />} 
            onClick={handleRefresh}
            loading={loading}
          >
            Refresh
          </Button>
          {lastUpdated && (
            <Text type="secondary" style={{ marginLeft: 16 }}>
              Last updated: {lastUpdated.toLocaleString()}
            </Text>
          )}
        </div>
      </div>

      <Divider />

      {insights.length === 0 ? (
        <Alert
          message="No Data"
          description="No patient insights available. Please check back later."
          type="info"
          showIcon
        />
      ) : (
        <div className="insights-grid">
          {insights.map((item) => (
            <Card 
              key={item.patient_id} 
              className="insight-card"
              title={
                <Space>
                  <span>Patient ID: {item.patient_id}</span>
                  {item.risk_score !== undefined && renderRiskBadge(item.risk_score)}
                </Space>
              }
              extra={
                <Text strong>Score: {item.risk_score || 'N/A'}</Text>
              }
            >
              <div className="insight-section">
                <Text strong>Clinical Insights:</Text>
                <div className="insight-content">
                  {item.clinical_insights || 'No insights available'}
                </div>
              </div>
              
              {item.patient_assessment && (
                <div className="insight-section">
                  <Text strong>Assessment:</Text>
                  <div className="assessment-content">
                    <pre>{JSON.stringify(item.patient_assessment, null, 2)}</pre>
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default PatientInsights;
