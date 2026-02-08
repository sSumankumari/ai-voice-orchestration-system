const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ApiService {
  constructor() {
    this.token = null;
  }

  setToken(token) {
    this.token = token;
  }

  getHeaders() {
    const headers = { 
      'Content-Type': 'application/json' 
    };
    
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    
    return headers;
  }

  async handleResponse(response) {
    if (!response.ok) {
      let errorMessage = 'Request failed';
      
      try {
        const error = await response.json();
        errorMessage = error.detail || error.message || JSON.stringify(error);
      } catch (e) {
        errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      }
      
      throw new Error(errorMessage);
    }
    
    // Handle 204 No Content
    if (response.status === 204) {
      return null;
    }
    
    return response.json();
  }

  // Authentication
  async login(username, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async register(username, email, password) {
    try {
      const response = await fetch(`${API_BASE_URL}/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    }
  }

  // Agents
  async getAgents() {
    try {
      const response = await fetch(`${API_BASE_URL}/agents/`, {
        headers: this.getHeaders(),
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Get agents error:', error);
      throw error;
    }
  }

  async getAgent(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/agents/${id}/`, {
        headers: this.getHeaders(),
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Get agent error:', error);
      throw error;
    }
  }

  async createAgent(agentData) {
    try {
      const response = await fetch(`${API_BASE_URL}/agents/`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify(agentData),
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Create agent error:', error);
      throw error;
    }
  }

  async updateAgent(id, agentData) {
    try {
      const response = await fetch(`${API_BASE_URL}/agents/${id}/`, {
        method: 'PUT',
        headers: this.getHeaders(),
        body: JSON.stringify(agentData),
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Update agent error:', error);
      throw error;
    }
  }

  async deleteAgent(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/agents/${id}/`, {
        method: 'DELETE',
        headers: this.getHeaders(),
      });
      return this.handleResponse(response);
    } catch (error) {
      console.error('Delete agent error:', error);
      throw error;
    }
  }
}

const api = new ApiService();
export default api;