import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, Layout, Spin } from 'antd';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import PatientInsights from './PatientInsights';
import Login from './pages/Login';
import './App.css';

const { Content } = Layout;

// Main App Layout
const AppLayout = () => {
  const { logout, user } = useAuth();

  return (
    <Layout className="app-layout">
      <Layout>
        <Content className="app-content">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <PatientInsights />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
};

// App component with providers
function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 4,
          colorLink: '#1890ff',
        },
      }}
    >
      <Router>
        <AuthProvider>
          <AppLayout />
        </AuthProvider>
      </Router>
    </ConfigProvider>
  );
}

export default App;
