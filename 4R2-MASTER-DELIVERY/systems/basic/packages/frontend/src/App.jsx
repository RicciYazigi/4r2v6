import React, { useState } from 'react';
import Dashboard from './components/Dashboard';

export default function App() {
  const [data, setData] = useState(null);
  const test = async () => {
    const res = await fetch('http://localhost:4000/api/coherence/measure', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        normative: [0.9, 0.8, 0.7, 0.6],
        representational: [0.85, 0.75, 0.65, 0.55],
        informational: [0.8, 0.7, 0.6, 0.5],
        physical: [1000, 8, 50, 10]
      })
    });
    setData(await res.json());
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #0f172a, #1e293b)', color: 'white', padding: '2rem' }}>
      <h1 style={{ textAlign: 'center', fontSize: '3rem' }}>4♻️2 Coherence Engine</h1>
      <button onClick={test} style={{
        width: '100%',
        padding: '1rem',
        background: '#3b82f6',
        border: 'none',
        borderRadius: '0.5rem',
        color: 'white',
        fontSize: '1.2rem',
        cursor: 'pointer',
        margin: '2rem 0'
      }}>
        🚀 Test Coherence
      </button>
      {data && <Dashboard data={data} />}
    </div>
  );
}
