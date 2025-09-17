import React, { useEffect } from 'react';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Spin, message } from 'antd';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading, checkAuth } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Check authentication status if not already loading
    if (!loading && !isAuthenticated) {
      const token = localStorage.getItem('token');
      if (token) {
        // If we have a token but not authenticated, try to validate it
        checkAuth();
      } else {
        // If no token, redirect to login immediately
        navigate('/login', { 
          state: { from: location },
          replace: true 
        });
      }
    }
  }, [isAuthenticated, loading, location, navigate, checkAuth]);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        flexDirection: 'column',
        gap: '16px'
      }}>
        <Spin size="large" />
        <p>Verifying your session...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    // If not authenticated and not loading, redirect to login
    return (
      <Navigate 
        to="/login" 
        state={{ 
          from: location,
          message: 'Please log in to access this page.'
        }} 
        replace 
      />
    );
  }

  return children;
};

export default ProtectedRoute;
