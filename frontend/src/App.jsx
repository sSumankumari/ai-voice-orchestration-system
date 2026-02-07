import { useState, useEffect } from 'react';
import AgentList from './components/AgentList';
import ChatInterface from './components/ChatInterface';
import Auth from './components/Auth';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showAuth, setShowAuth] = useState(false);

  useEffect(() => {
    // Check if user has a token
    const token = localStorage.getItem('token');
    if (token) {
      apiService.setToken(token);
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
    setShowAuth(false);
  };

  const handleLogout = () => {
    apiService.setToken(null);
    setIsAuthenticated(false);
    setSelectedAgent(null);
  };

  const handleSelectAgent = (agent) => {
    setSelectedAgent(agent);
  };

  if (showAuth) {
    return <Auth onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <div className="app-header">
        <div className="app-title">
          <h1>🤖 AI Voice Orchestration System</h1>
          <p>Real-time conversational AI with agentic architecture</p>
        </div>
        <div className="app-actions">
          {isAuthenticated ? (
            <>
              <span className="user-status">✓ Authenticated</span>
              <button onClick={handleLogout} className="btn-logout">
                Logout
              </button>
            </>
          ) : (
            <button onClick={() => setShowAuth(true)} className="btn-login-header">
              Login
            </button>
          )}
        </div>
      </div>

      <div className="app-content">
        <div className="sidebar">
          <AgentList 
            onSelectAgent={handleSelectAgent}
            selectedAgentId={selectedAgent?.id}
          />
        </div>
        <div className="main-content">
          <ChatInterface agent={selectedAgent} />
        </div>
      </div>
    </div>
  );
}

export default App;