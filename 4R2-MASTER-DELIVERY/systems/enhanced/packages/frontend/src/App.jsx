import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import SystemStatus from './components/SystemStatus';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:4000';

export default function App() {
  const [data, setData] = useState(null);
  const [systemState, setSystemState] = useState(null);
  const [sessionId, setSessionId] = useState(null);

  useEffect(() => {
    fetchSystemState();
    const interval = setInterval(fetchSystemState, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchSystemState = async () => {
    try {
      const res = await fetch(`${API_URL}/api/system/state`, {
        headers: sessionId ? { 'X-Session-Id': sessionId } : {}
      });
      const newSessionId = res.headers.get('X-Session-Id');
      if (newSessionId) setSessionId(newSessionId);
      setSystemState(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  const testCoherence = async () => {
    try {
      const res = await fetch(`${API_URL}/api/coherence/measure`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'X-Session-Id': sessionId || ''
        },
        body: JSON.stringify({
          normative: [0.9, 0.8, 0.7],
          representational: [0.85, 0.75, 0.65],
          informational: [0.8, 0.7, 0.6],
          physical: [1000, 8, 50, 10]
        })
      });
      setData(await res.json());
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a, #1e293b)', color: 'white', padding: '2rem' }}>
      <h1 style={{ textAlign: 'center', fontSize: '3rem', marginBottom: '1rem' }}>
        4♻️2 Coherence Engine ENHANCED
      </h1>
      <p style={{ textAlign: 'center', color: '#94a3b8', marginBottom: '2rem' }}>
        With Safety Monitor + Arming Protocol + Session Management
      </p>

      {systemState && <SystemStatus state={systemState} />}

      <button onClick={testCoherence} style={{
        width: '100%',
        padding: '1rem',
        background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
        border: 'none',
        borderRadius: '0.5rem',
        color: 'white',
        fontSize: '1.2rem',
        cursor: 'pointer',
        margin: '2rem 0'
      }}>
        🚀 Test Coherence (with Safety Monitor)
      </button>

      {data && <Dashboard data={data} />}
    </div>
  );
}
