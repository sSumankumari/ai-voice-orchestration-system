const API_BASE_URL = 'http://127.0.0.1:8000/api';
const WS_BASE_URL = 'ws://127.0.0.1:8001';

// API Service for Django REST endpoints
class ApiService {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  setToken(token) {
    this.token = token;
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }

  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  // Authentication
  async login(username, password) {
    const response = await fetch(`${API_BASE_URL}/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!response.ok) throw new Error('Login failed');
    const data = await response.json();
    this.setToken(data.access);
    return data;
  }

  async refreshToken(refreshToken) {
    const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    if (!response.ok) throw new Error('Token refresh failed');
    const data = await response.json();
    this.setToken(data.access);
    return data;
  }

  // Agents
  async getAgents() {
    const response = await fetch(`${API_BASE_URL}/agents/`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error('Failed to fetch agents');
    return response.json();
  }

  async getAgent(id) {
    const response = await fetch(`${API_BASE_URL}/agents/${id}/`, {
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error('Failed to fetch agent');
    return response.json();
  }

  async createAgent(agentData) {
    const response = await fetch(`${API_BASE_URL}/agents/`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(agentData),
    });
    if (!response.ok) throw new Error('Failed to create agent');
    return response.json();
  }

  async updateAgent(id, agentData) {
    const response = await fetch(`${API_BASE_URL}/agents/${id}/`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(agentData),
    });
    if (!response.ok) throw new Error('Failed to update agent');
    return response.json();
  }

  async deleteAgent(id) {
    const response = await fetch(`${API_BASE_URL}/agents/${id}/`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });
    if (!response.ok) throw new Error('Failed to delete agent');
  }
}

// WebSocket Service for real-time chat
class WebSocketService {
  constructor() {
    this.ws = null;
    this.onMessage = null;
    this.onConnect = null;
    this.onDisconnect = null;
    this.onError = null;
  }

  connect(agentId) {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(`${WS_BASE_URL}/ws/chat/${agentId}`);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        resolve();
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received:', data);
        
        if (data.type === 'connected' && this.onConnect) {
          this.onConnect(data);
        } else if (data.type === 'response' && this.onMessage) {
          this.onMessage(data);
        } else if (data.type === 'error' && this.onError) {
          this.onError(data);
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (this.onError) {
          this.onError({ message: 'WebSocket connection error' });
        }
        reject(error);
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        if (this.onDisconnect) {
          this.onDisconnect();
        }
      };
    });
  }

  sendMessage(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(message);
    } else {
      console.error('WebSocket is not connected');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  isConnected() {
    return this.ws && this.ws.readyState === WebSocket.OPEN;
  }
}

const apiService = new ApiService();
const wsService = new WebSocketService();

export { apiService, wsService, WS_BASE_URL };