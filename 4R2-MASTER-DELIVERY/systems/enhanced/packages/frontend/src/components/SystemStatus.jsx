import React from 'react';

export default function SystemStatus({ state }) {
  const { session, safety } = state;
  
  const getStateColor = () => {
    if (session.armed) return '#10b981';
    if (session.state === 'LOCKED') return '#ef4444';
    return '#f59e0b';
  };

  return (
    <div style={{ 
      background: 'rgba(255,255,255,0.05)', 
      borderRadius: '1rem', 
      padding: '1.5rem',
      marginBottom: '2rem',
      border: `2px solid ${getStateColor()}`
    }}>
      <h3 style={{ marginBottom: '1rem' }}>🔒 System Status</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
        <div>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Session State</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: getStateColor() }}>
            {session.state}
          </div>
        </div>
        <div>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Safety Status</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
            {safety.status}
          </div>
        </div>
        <div>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Total Measurements</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
            {safety.total_measurements}
          </div>
        </div>
        <div>
          <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Avg Quality (Recent)</div>
          <div style={{ fontSize: '1.2rem', fontWeight: 'bold' }}>
            {safety.avg_quality_recent?.toFixed(4) || 'N/A'}
          </div>
        </div>
      </div>
    </div>
  );
}
