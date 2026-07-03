import dotenv from 'dotenv';
dotenv.config();

export const config = {
    llmProvider: process.env.LLM_PROVIDER || 'mock',
    geminiApiKey: process.env.GEMINI_API_KEY || '',
    basicKernelUrl: process.env.BASIC_KERNEL_URL || 'http://localhost:8000',
    basicBackendUrl: process.env.BASIC_BACKEND_URL || 'http://localhost:4000',
    dbBridgeUrl: process.env.DB_BRIDGE_URL || 'http://localhost:4001',
    temperature: parseFloat(process.env.TEMPERATURE || '0'),
    topP: parseFloat(process.env.TOP_P || '1'),
    hardGateMin: parseFloat(process.env.HARD_GATE_MIN || '0.66'),
    evidenceDir: process.env.EVIDENCE_DIR || './evidence',

    // Normalization Refs (Audit-Grade Calibration)
    LAT_REF_MS: 5000,    // 5s baseline for high latency
    TPS_REF: 100,        // 100 tokens/sec
    MEM_REF_MB: 512,     // 512MB
    COST_REF_USD: 0.1,   // $0.10
};
