import React from 'react';

export default function Dashboard({ data }) {
  const metrics = [
    { name: 'C_NR', value: data.C_NR },
    { name: 'C_RI', value: data.C_RI },
    { name: 'C_IF', value: data.C_IF },
    { name: 'C_total', value: data.C_total },
    { name: 'Quality Score', value: data.quality_score },
    { name: 'Entropy Loss', value: data.entropy_loss }
  ];

  const safetyColor = () => {
    const action = data.safety_check?.action;
    if (action === 'BLOCK') return '#ef4444';
    if (action === 'WARN') return '#f59e0b';
    return '#10b981';
  };

  return (
    <div style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '1rem', padding: '2rem' }}>
      <h2 style={{ marginBottom: '1.5rem' }}>📊 Coherence Metrics</h2>
      
      {data.safety_check && (
        <div style={{
          marginBottom: '1.5rem',
          padding: '1rem',
          background: `rgba(${safetyColor()}, 0.1)`,
          borderLeft: `4px solid ${safetyColor()}`,
          borderRadius: '0.5rem'
        }}>
          <strong>Safety Check:</strong> {data.safety_check.action} 
          {data.safety_check.reason && ` (${data.safety_check.reason})`}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
        {metrics.map(m => (
          <div key={m.name} style={{
            background: 'rgba(255,255,255,0.08)',
            padding: '1rem',
            borderRadius: '0.5rem'
          }}>
            <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>{m.name}</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
              {m.value?.toFixed(4) || 'N/A'}
            </div>
          </div>
        ))}
      </div>

      <div style={{ marginTop: '1.5rem', fontSize: '0.9rem', color: '#94a3b8' }}>
        Trace ID: <code>{data.trace_id}</code>
      </div>
    </div>
  );
}
