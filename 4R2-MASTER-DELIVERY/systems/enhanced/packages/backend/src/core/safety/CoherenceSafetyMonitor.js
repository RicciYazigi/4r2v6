/**
 * GATE E: Coherence Safety Monitor
 * Bloquea respuestas con coherencia en DANGER o SINGULARITY
 */

export class CoherenceSafetyMonitor {
  constructor() {
    this.history = [];
    this.SINGULARITY_THRESHOLD = 0.0;
    this.DANGER_THRESHOLD = 0.1;
  }

  checkCoherence(coherence, trace_id) {
    const { C_total, quality_score } = coherence;
    
    // Detectar singularidad (coherencia negativa o muy baja)
    if (quality_score < this.SINGULARITY_THRESHOLD) {
      console.error(`[${trace_id}] ❌ SINGULARITY DETECTED: quality=${quality_score}`);
      return {
        action: 'BLOCK',
        reason: 'SINGULARITY',
        severity: 'CRITICAL'
      };
    }
    
    // Detectar peligro
    if (quality_score < this.DANGER_THRESHOLD) {
      console.warn(`[${trace_id}] ⚠️  DANGER ZONE: quality=${quality_score}`);
      return {
        action: 'WARN',
        reason: 'DANGER',
        severity: 'HIGH'
      };
    }
    
    // Todo OK
    this.history.push({ trace_id, C_total, quality_score, timestamp: Date.now() });
    return {
      action: 'CONTINUE',
      reason: 'OK',
      severity: 'NONE'
    };
  }

  getSystemState() {
    const recent = this.history.slice(-10);
    const avgQuality = recent.length > 0
      ? recent.reduce((sum, h) => sum + h.quality_score, 0) / recent.length
      : 0;
    
    return {
      total_measurements: this.history.length,
      avg_quality_recent: avgQuality,
      status: avgQuality > 0.5 ? 'HEALTHY' : avgQuality > 0.1 ? 'DEGRADED' : 'CRITICAL'
    };
  }

  resetHistory() {
    this.history = [];
  }
}
