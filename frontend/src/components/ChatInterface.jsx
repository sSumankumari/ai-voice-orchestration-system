import { useState, useEffect, useRef } from 'react';
import { wsService } from '../services/api';
import './ChatInterface.css';

function ChatInterface({ agent }) {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [connected, setConnected] = useState(false);
  const [sessionInfo, setSessionInfo] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (agent) {
      connectToAgent();
    }

    return () => {
      wsService.disconnect();
    };
  }, [agent]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const connectToAgent = async () => {
    try {
      setMessages([]);
      setError(null);
      setConnected(false);

      wsService.onConnect = (data) => {
        setConnected(true);
        setSessionInfo(data);
        setMessages([{
          type: 'system',
          text: `Connected to ${agent.name} (${data.category})`,
          timestamp: new Date(),
        }]);
      };

      wsService.onMessage = (data) => {
        setIsTyping(false);
        setMessages(prev => [...prev, {
          type: 'agent',
          text: data.message,
          intent: data.intent,
          timestamp: new Date(),
        }]);
      };

      wsService.onError = (data) => {
        setIsTyping(false);
        setError(data.message);
        setMessages(prev => [...prev, {
          type: 'error',
          text: data.message,
          timestamp: new Date(),
        }]);
      };

      wsService.onDisconnect = () => {
        setConnected(false);
        setMessages(prev => [...prev, {
          type: 'system',
          text: 'Disconnected from agent',
          timestamp: new Date(),
        }]);
      };

      await wsService.connect(agent.id);
    } catch (err) {
      setError('Failed to connect to agent');
      console.error('Connection error:', err);
    }
  };

  const sendMessage = (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || !connected) return;

    const userMessage = inputMessage.trim();
    setMessages(prev => [...prev, {
      type: 'user',
      text: userMessage,
      timestamp: new Date(),
    }]);

    wsService.sendMessage(userMessage);
    setInputMessage('');
    setIsTyping(true);
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  if (!agent) {
    return (
      <div className="chat-interface-empty">
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h2>No Agent Selected</h2>
          <p>Select an agent from the sidebar to start chatting</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-header-info">
          <h2>{agent.name}</h2>
          <span className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
            {connected ? '● Connected' : '○ Disconnected'}
          </span>
        </div>
        {sessionInfo && (
          <div className="session-info">
            <span>Session: {sessionInfo.session_id.substring(0, 8)}...</span>
          </div>
        )}
      </div>

      {error && (
        <div className="chat-error">
          {error}
          <button onClick={connectToAgent}>Retry</button>
        </div>
      )}

      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message message-${msg.type}`}>
            {msg.type === 'user' && (
              <div className="message-content user-message">
                <div className="message-bubble">
                  <p>{msg.text}</p>
                  <span className="message-time">{formatTime(msg.timestamp)}</span>
                </div>
              </div>
            )}
            
            {msg.type === 'agent' && (
              <div className="message-content agent-message">
                <div className="message-bubble">
                  <p>{msg.text}</p>
                  <div className="message-footer">
                    <span className="message-intent">Intent: {msg.intent}</span>
                    <span className="message-time">{formatTime(msg.timestamp)}</span>
                  </div>
                </div>
              </div>
            )}
            
            {msg.type === 'system' && (
              <div className="message-content system-message">
                <span>{msg.text}</span>
              </div>
            )}
            
            {msg.type === 'error' && (
              <div className="message-content error-message">
                <span>⚠️ {msg.text}</span>
              </div>
            )}
          </div>
        ))}
        
        {isTyping && (
          <div className="message message-agent">
            <div className="message-content agent-message">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <form className="chat-input-form" onSubmit={sendMessage}>
        <input
          ref={inputRef}
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={connected ? "Type your message..." : "Connecting..."}
          disabled={!connected}
        />
        <button 
          type="submit" 
          disabled={!connected || !inputMessage.trim()}
          className="btn-send"
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;