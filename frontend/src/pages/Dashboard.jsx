import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './Dashboard.css';

const CATEGORIES = [
  'medical', 'nutrition', 'finance', 'legal', 'research', 'interview', 'general'
];

const CATEGORY_ICONS = {
  medical: '🏥',
  nutrition: '🥗',
  finance: '💰',
  legal: '⚖️',
  research: '🔬',
  interview: '💼',
  general: '💬'
};

function Dashboard({ token, onLogout }) {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    category: 'general',
    system_prompt: ''
  });
  const [creating, setCreating] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    api.setToken(token);
    loadAgents();
  }, [token]);

  const loadAgents = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await api.getAgents();
      setAgents(data);
    } catch (err) {
      setError('Failed to load agents: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAgent = async (e) => {
    e.preventDefault();
    
    if (!newAgent.name.trim() || !newAgent.system_prompt.trim()) {
      setError('Please fill in all fields');
      return;
    }

    setCreating(true);
    setError('');

    try {
      await api.createAgent(newAgent);
      setNewAgent({ name: '', category: 'general', system_prompt: '' });
      setShowCreateForm(false);
      loadAgents();
    } catch (err) {
      setError('Failed to create agent: ' + err.message);
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteAgent = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete "${name}"?`)) return;
    
    try {
      setError('');
      await api.deleteAgent(id);
      loadAgents();
    } catch (err) {
      setError('Failed to delete agent: ' + err.message);
    }
  };

  const startChat = (agentId) => {
    navigate(`/chat/${agentId}`);
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-left">
          <h1>🤖 AI Agents Dashboard</h1>
          <p className="header-subtitle">{agents.length} agent{agents.length !== 1 ? 's' : ''} available</p>
        </div>
        <button onClick={onLogout} className="btn btn-secondary">
          Logout
        </button>
      </header>

      {error && (
        <div className="dashboard-content">
          <div className="error-message">
            {error}
            <button onClick={() => setError('')} style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer' }}>✕</button>
          </div>
        </div>
      )}

      <div className="dashboard-content">
        <div className="actions-bar">
          <button 
            onClick={() => setShowCreateForm(!showCreateForm)} 
            className="btn btn-primary"
          >
            {showCreateForm ? '✕ Cancel' : '+ Create New Agent'}
          </button>
        </div>

        {showCreateForm && (
          <div className="create-agent-form">
            <h2>Create New AI Agent</h2>
            <form onSubmit={handleCreateAgent}>
              <div className="form-group">
                <label htmlFor="agentName">Agent Name</label>
                <input
                  id="agentName"
                  type="text"
                  value={newAgent.name}
                  onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
                  placeholder="e.g., Medical Assistant, Finance Advisor"
                  required
                  autoFocus
                />
              </div>

              <div className="form-group">
                <label htmlFor="agentCategory">Category</label>
                <select
                  id="agentCategory"
                  value={newAgent.category}
                  onChange={(e) => setNewAgent({ ...newAgent, category: e.target.value })}
                  required
                >
                  {CATEGORIES.map(cat => (
                    <option key={cat} value={cat}>
                      {CATEGORY_ICONS[cat]} {cat.charAt(0).toUpperCase() + cat.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="systemPrompt">System Prompt</label>
                <textarea
                  id="systemPrompt"
                  value={newAgent.system_prompt}
                  onChange={(e) => setNewAgent({ ...newAgent, system_prompt: e.target.value })}
                  placeholder="Define the agent's behavior, expertise, and personality..."
                  rows="6"
                  required
                />
                <small className="form-hint">
                  Example: "You are a helpful medical assistant specializing in general health advice..."
                </small>
              </div>

              <button type="submit" className="btn btn-primary btn-block" disabled={creating}>
                {creating ? 'Creating Agent...' : 'Create Agent'}
              </button>
            </form>
          </div>
        )}

        {loading ? (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading agents...</p>
          </div>
        ) : agents.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🤖</div>
            <h3>No Agents Yet</h3>
            <p>Create your first AI agent to get started!</p>
            {!showCreateForm && (
              <button 
                onClick={() => setShowCreateForm(true)} 
                className="btn btn-primary"
                style={{ marginTop: '20px' }}
              >
                + Create First Agent
              </button>
            )}
          </div>
        ) : (
          <div className="agents-grid">
            {agents.map(agent => (
              <div key={agent.id} className="agent-card">
                <div className="agent-header">
                  <h3>
                    {CATEGORY_ICONS[agent.category] || '💬'} {agent.name}
                  </h3>
                  <span className={`category-badge badge-${agent.category}`}>
                    {agent.category}
                  </span>
                </div>
                <p className="agent-prompt">
                  {agent.system_prompt.length > 150 
                    ? agent.system_prompt.substring(0, 150) + '...' 
                    : agent.system_prompt}
                </p>
                <div className="agent-meta">
                  <small>ID: {agent.id}</small>
                  <small>Created: {new Date(agent.created_at).toLocaleDateString()}</small>
                </div>
                <div className="agent-actions">
                  <button 
                    onClick={() => startChat(agent.id)} 
                    className="btn btn-primary btn-sm"
                  >
                    💬 Start Chat
                  </button>
                  <button 
                    onClick={() => handleDeleteAgent(agent.id, agent.name)} 
                    className="btn btn-danger btn-sm"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;