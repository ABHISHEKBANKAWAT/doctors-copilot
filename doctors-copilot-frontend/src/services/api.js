const API_BASE_URL = 'http://localhost:5000/api';

// Helper function to handle API responses
async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.message || 'Something went wrong');
  }
  return response.json();
}

// Auth API
export const authAPI = {
  login: async (username, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    return handleResponse(response);
  },
};

// Patient Insights API
export const patientAPI = {
  getInsights: async (token, page = 1, perPage = 10) => {
    const headers = {
      'Content-Type': 'application/json',
    };

    // Only add Authorization header if token is provided
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(
      `${API_BASE_URL}/patient_insights?page=${page}&per_page=${perPage}`,
      {
        headers,
        credentials: 'include',  // Include cookies in the request
      }
    );
    
    return handleResponse(response);
  },
};

// Health Check API
export const systemAPI = {
  healthCheck: async () => {
    const response = await fetch(`${API_BASE_URL}/health`);
    return handleResponse(response);
  },
};
