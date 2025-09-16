import React, { createContext, useState, useContext, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { message } from 'antd';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const location = useLocation();

  // Check for existing token on initial load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // In a real app, you would validate the token with the server
      setUser({ token });
    }
    setLoading(false);
  }, []);

  // Login function
  const login = async (username, password) => {
    try {
      const data = await authAPI.login(username, password);
      if (data && data.access_token) {
        localStorage.setItem('token', data.access_token);
        setUser({ token: data.access_token });
        message.success('Login successful');
        return true;
      }
    } catch (error) {
      message.error(error.message || 'Login failed');
      return false;
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate('/login');
    message.success('Logged out successfully');
  };

  // Get auth header
  const getAuthHeader = () => {
    const token = user?.token || localStorage.getItem('token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  };

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!loading && !user && location.pathname !== '/login') {
      navigate('/login');
    }
  }, [user, loading, location, navigate]);

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
    getAuthHeader,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
