import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './AgentList.css';

const CATEGORIES = [
  'medical', 'nutrition', 'finance', 'legal', 
  'research', 'interview', 'general'
];

function AgentList({ onSelectAgent, selectedAgentId }) {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    category: 'general',
    system_prompt: '',
  });

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setLoading(true);
      const data = await apiService.getAgents();
      setAgents(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAgent = async (e) => {
    e.preventDefault();
    try {
      await apiService.createAgent(newAgent);
      setNewAgent({ name: '', category: 'general', system_prompt: '' });
      setShowCreateForm(false);
      loadAgents();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteAgent = async (id) => {
    if (!window.confirm('Are you sure you want to delete this agent?')) return;
    try {
      await apiService.deleteAgent(id);
      loadAgents();
    } catch (err) {
      setError(err.message);
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      medical: '#e74c3c',
      nutrition: '#2ecc71',
      finance: '#3498db',
      legal: '#9b59b6',
      research: '#e67e22',
      interview: '#1abc9c',
      general: '#95a5a6',
    };
    return colors[category] || colors.general;
  };

  if (loading) {
    return <div className="agent-list-loading">Loading agents...</div>;
  }

  return (
    <div className="agent-list">
      <div className="agent-list-header">
        <h2>AI Agents</h2>
        <button 
          className="btn-create"
          onClick={() => setShowCreateForm(!showCreateForm)}
        >
          {showCreateForm ? '✕ Cancel' : '+ New Agent'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showCreateForm && (
        <form className="create-agent-form" onSubmit={handleCreateAgent}>
          <input
            type="text"
            placeholder="Agent name"
            value={newAgent.name}
            onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
            required
          />
          <select
            value={newAgent.category}
            onChange={(e) => setNewAgent({ ...newAgent, category: e.target.value })}
            required
          >
            {CATEGORIES.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          <textarea
            placeholder="System prompt (defines agent behavior)"
            value={newAgent.system_prompt}
            onChange={(e) => setNewAgent({ ...newAgent, system_prompt: e.target.value })}
            rows={4}
            required
          />
          <button type="submit" className="btn-submit">Create Agent</button>
        </form>
      )}

      <div className="agents-grid">
        {agents.length === 0 ? (
          <div className="no-agents">
            <p>No agents found. Create one to get started!</p>
          </div>
        ) : (
          agents.map(agent => (
            <div 
              key={agent.id} 
              className={`agent-card ${selectedAgentId === agent.id ? 'selected' : ''}`}
              onClick={() => onSelectAgent(agent)}
            >
              <div className="agent-card-header">
                <h3>{agent.name}</h3>
                <button
                  className="btn-delete"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteAgent(agent.id);
                  }}
                >
                  🗑️
                </button>
              </div>
              <div 
                className="agent-category"
                style={{ backgroundColor: getCategoryColor(agent.category) }}
              >
                {agent.category}
              </div>
              <p className="agent-prompt">{agent.system_prompt}</p>
              <div className="agent-meta">
                <span>ID: {agent.id}</span>
                <span>{new Date(agent.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default AgentList;