import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AgentChat from './pages/AgentChat';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={!token ? <Login onLogin={handleLogin} /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/register"
          element={!token ? <Register onLogin={handleLogin} /> : <Navigate to="/dashboard" />}
        />
        <Route
          path="/dashboard"
          element={token ? <Dashboard token={token} onLogout={handleLogout} /> : <Navigate to="/login" />}
        />
        <Route
          path="/chat/:agentId"
          element={token ? <AgentChat token={token} onLogout={handleLogout} /> : <Navigate to="/login" />}
        />
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;