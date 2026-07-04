import { config } from '../config.js';

export interface PhysicalObservables {
    latency_ms: number;
    tokens_per_sec: number;
    memory_delta_mb: number;
    cost_normalized: number;
}

const clamp = (val: number, min: number, max: number) => Math.min(Math.max(val, min), max);

export function calculatePhysicalVector(obs: PhysicalObservables): number[] {
    // Audit-Grade Calibration (STRICT 1240421 Contract)
    return [
        clamp(obs.latency_ms / config.LAT_REF_MS, 0, 1),
        clamp(obs.tokens_per_sec / config.TPS_REF, 0, 1),
        clamp(obs.memory_delta_mb / config.MEM_REF_MB, 0, 1),
        clamp(obs.cost_normalized, 0, 1)
    ];
}

export function calculateKLRaw(p: number[], q: number[]): number {
    // Manual KL Divergence (High Resolution - No Cap)
    let kl = 0;
    for (let i = 0; i < p.length; i++) {
        const pi = p[i] || 1e-10; // Avoid log(0)
        const qi = q[i] || 1e-10;
        kl += pi * Math.log(pi / qi);
    }
    return kl;
}

export function stringToVector(str: string): number[] {
    /**
     * 4R2 SEMANTIC HASHING (STRICT 1240421 Contract)
     * Mapea el texto a 4 dimensiones conceptuales:
     * [0] Estructura/Complejidad
     * [1] Tono/Sentimiento (Proxy)
     * [2] Densidad de Información
     * [3] Especificidad/Datos
     */
    const vec = [0.25, 0.25, 0.25, 0.25];
    if (!str) return vec;

    const text = str.toLowerCase();
    const words = text.split(/\s+/);
    const len = text.length || 1;
    const wordCount = words.length || 1;

    // 1. Estructura/Complejidad (Basado en longitud de palabras y puntuación)
    const avgWordLen = text.replace(/\s/g, '').length / wordCount;
    const punctuationCount = (text.match(/[.,!?;:]/g) || []).length;
    vec[0] = (avgWordLen / 10) * 0.7 + (punctuationCount / wordCount) * 0.3;

    // 2. Tono/Sentimiento (Proxy basado en palabras clave positivas/negativas)
    const posWords = ['bueno', 'excelente', 'estabilidad', 'coherencia', 'éxito', 'seguro', 'stable', 'coherence', 'success', 'safe'];
    const negWords = ['error', 'fallo', 'inestable', 'riesgo', 'peligro', 'fail', 'unstable', 'risk', 'danger'];
    let sentiment = 0.5;
    words.forEach(w => {
        if (posWords.includes(w)) sentiment += 0.05;
        if (negWords.includes(w)) sentiment -= 0.05;
    });
    vec[1] = Math.max(0, Math.min(1, sentiment));

    // 3. Densidad de Información (Palabras únicas vs totales)
    const uniqueWords = new Set(words).size;
    vec[2] = uniqueWords / wordCount;

    // 4. Especificidad/Datos (Presencia de números y mayúsculas)
    const digitDensity = (text.match(/[0-9]/g) || []).length / len;
    const upperDensity = (str.match(/[A-Z]/g) || []).length / len;
    vec[3] = Math.min(1, (digitDensity * 5) + (upperDensity * 2));

    // Normalización final para asegurar estabilidad en el Kernel
    const sum = vec.reduce((a, b) => a + b, 0) || 1;
    return vec.map(v => Math.max(0.01, v / sum)); // Evitamos ceros absolutos para estabilidad KL
}
