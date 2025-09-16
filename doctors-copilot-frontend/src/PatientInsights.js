import React, { useEffect, useState, useCallback } from 'react';
import { Card, Spin, Alert, Button, Typography, Divider, Space, message } from 'antd';
import { ReloadOutlined, LogoutOutlined } from '@ant-design/icons';
import { useAuth } from './contexts/AuthContext';
import { patientAPI } from './services/api';
import './PatientInsights.css';

const { Title, Text } = Typography;

const PatientInsights = () => {
  const { logout, getAuthHeader } = useAuth();
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  const fetchInsights = useCallback(async (page = 1, pageSize = 10) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await patientAPI.getInsights(
        localStorage.getItem('token'),
        page,
        pageSize
      );
      
      if (response.success) {
        setInsights(response.data);
        setPagination({
          ...pagination,
          current: page,
          pageSize,
          total: response.pagination?.total_items || 0,
        });
        setLastUpdated(new Date());
      } else {
        throw new Error(response.error || 'Failed to fetch patient insights');
      }
    } catch (err) {
      console.error('Error fetching insights:', err);
      setError(`Failed to load patient insights: ${err.message}`);
      message.error(`Failed to load patient insights: ${err.message}`);
      
      // If unauthorized, log out the user
      if (err.message.includes('401')) {
        message.warning('Your session has expired. Please log in again.');
        logout();
      }
    } finally {
      setLoading(false);
    }
  }, [pagination, logout]);

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

  const handleTableChange = (pagination, filters, sorter) => {
    fetchInsights(pagination.current, pagination.pageSize);
  };

  return (
    <div className="patient-insights-container">
      <div className="header-section">
        <div>
          <Title level={2} style={{ marginBottom: 0 }}>Patient Insights</Title>
          <Text type="secondary">Comprehensive patient data analysis</Text>
        </div>
        <div className="controls">
          <Space>
            <Button 
              type="primary" 
              icon={<ReloadOutlined />} 
              onClick={() => fetchInsights(pagination.current, pagination.pageSize)}
              loading={loading}
            >
              Refresh
            </Button>
            <Button
              icon={<LogoutOutlined />}
              onClick={() => {
                logout();
                message.success('Successfully logged out');
              }}
            >
              Logout
            </Button>
            {lastUpdated && (
              <Text type="secondary" style={{ marginLeft: 8 }}>
                Last updated: {lastUpdated.toLocaleString()}
              </Text>
            )}
          </Space>
        </div>
      </div>

      <Divider />

      {insights.length === 0 && !loading ? (
        <Alert
          message="No Data"
          description="No patient insights available. Please check back later."
          type="info"
          showIcon
          style={{ marginTop: 16 }}
        />
      ) : (
        <div className="insights-grid">
          {insights.map((item) => (
            <Card 
              key={`${item.patient_id}-${item.admission_id}`} 
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
              loading={loading}
              style={{ marginBottom: 16 }}
            >
              <div className="insight-section">
                <Text strong>Admission:</Text>
                <div className="insight-content">
                  <div>Type: {item.admission_type || 'N/A'}</div>
                  <div>Diagnosis: {item.diagnosis || 'Not specified'}</div>
                  <div>Admission Date: {item.admission_date || 'N/A'}</div>
                  {item.discharge_date && (
                    <div>Discharge Date: {item.discharge_date}</div>
                  )}
                </div>
              </div>

              <div className="insight-section">
                <Text strong>Vital Signs:</Text>
                <div className="insight-content">
                  <div>Heart Rate: {item.vital_signs?.heart_rate || 'N/A'} bpm</div>
                  <div>Blood Pressure: 
                    {item.vital_signs?.systolic_bp && item.vital_signs?.diastolic_bp 
                      ? `${item.vital_signs.systolic_bp}/${item.vital_signs.diastolic_bp} mmHg` 
                      : 'N/A'}
                  </div>
                </div>
              </div>

              <div className="insight-section">
                <Text strong>Lab Results:</Text>
                <div className="insight-content">
                  <div>Glucose: {item.lab_results?.glucose || 'N/A'} mg/dL</div>
                  <div>Creatinine: {item.lab_results?.creatinine || 'N/A'} mg/dL</div>
                </div>
              </div>
              
              {item.patient_assessment && (
                <div className="insight-section">
                  <Divider style={{ margin: '12px 0' }} />
                  <div className="assessment-section">
                    <Text strong>Assessment:</Text>
                    <div className="assessment-details">
                      <div>
                        <Text strong>Concern Level: </Text>
                        <span className={`concern-${item.patient_assessment.concern_level?.toLowerCase() || 'low'}`}>
                          {item.patient_assessment.concern_level || 'Low'}
                        </span>
                      </div>
                      
                      {item.patient_assessment.key_findings?.length > 0 && (
                        <div style={{ marginTop: 8 }}>
                          <Text strong>Key Findings:</Text>
                          <ul style={{ margin: '4px 0 0 0', paddingLeft: 20 }}>
                            {item.patient_assessment.key_findings.map((finding, idx) => (
                              <li key={idx}>{finding}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {item.patient_assessment.recommendations?.length > 0 && (
                        <div style={{ marginTop: 8 }}>
                          <Text strong>Recommendations:</Text>
                          <ul style={{ margin: '4px 0 0 0', paddingLeft: 20 }}>
                            {item.patient_assessment.recommendations.map((rec, idx) => (
                              <li key={idx}>{rec}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
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
