import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import './AgentChat.css';

const WS_BASE_URL = 'ws://127.0.0.1:8001';

function AgentChat({ token, onLogout }) {
  const { agentId } = useParams();
  const navigate = useNavigate();
  const [agent, setAgent] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [connected, setConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState('');
  const wsRef = useRef(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    api.setToken(token);
    loadAgent();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [agentId, token]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadAgent = async () => {
    try {
      const data = await api.getAgent(agentId);
      setAgent(data);
      connectWebSocket();
    } catch (err) {
      setError('Failed to load agent: ' + err.message);
    }
  };

  const connectWebSocket = () => {
    try {
      const ws = new WebSocket(`${WS_BASE_URL}/ws/chat/${agentId}`);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('✅ WebSocket connected');
        setConnected(true);
        setError('');
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('📨 Received:', data);

        if (data.type === 'connected') {
          addMessage('system', `✅ Connected to ${data.category} agent. Session: ${data.session_id.substring(0, 8)}...`);
        } else if (data.type === 'response') {
          setIsTyping(false);
          addMessage('agent', data.message, data.intent);
        } else if (data.type === 'error') {
          setIsTyping(false);
          setError(data.message);
          addMessage('error', data.message);
        }
      };

      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        setError('Connection error. Make sure FastAPI is running on port 8001.');
        setConnected(false);
      };

      ws.onclose = () => {
        console.log('🔌 WebSocket closed');
        setConnected(false);
        addMessage('system', '🔴 Disconnected from agent');
      };
    } catch (err) {
      setError('Failed to connect: ' + err.message);
    }
  };

  const addMessage = (type, text, intent = null) => {
    setMessages(prev => [...prev, {
      type,
      text,
      intent,
      timestamp: new Date()
    }]);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || !connected) return;

    const userMsg = inputMessage.trim();
    addMessage('user', userMsg);
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(userMsg);
      setIsTyping(true);
    } else {
      setError('Not connected to agent');
    }

    setInputMessage('');
    inputRef.current?.focus();
  };

  const handleBack = () => {
    if (wsRef.current) {
      wsRef.current.close();
    }
    navigate('/dashboard');
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <button onClick={handleBack} className="btn btn-secondary btn-sm">
          ← Back to Dashboard
        </button>
        <div className="chat-info">
          <h2>{agent?.name || 'Loading...'}</h2>
          <span className={`status ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? '🟢 Connected' : '🔴 Disconnected'}
          </span>
        </div>
        <button onClick={onLogout} className="btn btn-secondary btn-sm">
          Logout
        </button>
      </header>

      {error && (
        <div className="error-banner">
          ⚠️ {error}
          <button onClick={() => setError('')} className="close-btn">✕</button>
        </div>
      )}

      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h3>👋 Welcome!</h3>
            <p>Start a conversation with {agent?.name}</p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`message message-${msg.type}`}>
            <div className="message-content">
              <p>{msg.text}</p>
              {msg.intent && (
                <div className="message-meta">
                  <span className="message-intent">
                    🎯 Intent: <strong>{msg.intent}</strong>
                  </span>
                  <span className="message-time">{formatTime(msg.timestamp)}</span>
                </div>
              )}
              {!msg.intent && msg.type !== 'system' && (
                <span className="message-time">{formatTime(msg.timestamp)}</span>
              )}
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="message message-agent">
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="chat-input-form">
        <input
          ref={inputRef}
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={connected ? "Type your message..." : "Connecting to agent..."}
          disabled={!connected}
          className="chat-input"
        />
        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={!connected || !inputMessage.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default AgentChat;