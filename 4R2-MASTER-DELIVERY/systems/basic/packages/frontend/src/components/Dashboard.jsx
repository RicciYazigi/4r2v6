import React from 'react';
export default function Dashboard({ data }) {
  return (
    <div style={{ background: 'rgba(255,255,255,0.05)', borderRadius: '1rem', padding: '2rem' }}>
      <h2>📊 Metrics</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginTop: '1rem' }}>
        <MetricCard label="C_NR" value={data.C_NR} />
        <MetricCard label="C_RI" value={data.C_RI} />
        <MetricCard label="C_IF" value={data.C_IF} />
        <MetricCard label="C_total" value={data.C_total} />
        <MetricCard label="Quality" value={data.quality_score} />
        <MetricCard label="Entropy" value={data.entropy_loss} />
      </div>
    </div>
  );
}

function MetricCard({ label, value }) {
  return (
    <div style={{ background: 'rgba(255,255,255,0.08)', padding: '1rem', borderRadius: '0.5rem' }}>
      <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>{label}</div>
      <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{value?.toFixed(4) || 'N/A'}</div>
    </div>
  );
}
