import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
import { CoherenceSafetyMonitor } from './core/safety/CoherenceSafetyMonitor.js';
import { SessionManager } from './security/sessionManager.js';

dotenv.config();

const app = express();
const KERNEL_URL = process.env.KERNEL_URL || 'http://kernel:8000';

const safetyMonitor = new CoherenceSafetyMonitor();
const sessionManager = new SessionManager();

// SIMPLE RATE LIMITER (60 req/min)
const RATE_LIMIT = 60;
const RATE_WINDOW = 60000;
const clients = new Map();

app.use((req, res, next) => {
  const ip = req.ip;
  const now = Date.now();
  if (!clients.has(ip)) clients.set(ip, []);
  const timestamps = clients.get(ip).filter(t => now - t < RATE_WINDOW);
  timestamps.push(now);
  clients.set(ip, timestamps);
  if (timestamps.length > RATE_LIMIT) {
    return res.status(429).json({ error: 'RATE_LIMIT_EXCEEDED', detail: 'Maximum 60 requests per minute' });
  }
  next();
});

app.use(cors());
app.use(express.json());

// Middleware de sesión
app.use((req, res, next) => {
  let sessionId = req.headers['x-session-id'];
  if (!sessionId) {
    sessionId = `session_${Date.now()}`;
    res.setHeader('X-Session-Id', sessionId);
  }
  if (!sessionManager.getSession(sessionId)) {
    sessionManager.createSession(sessionId);
  }
  req.sessionId = sessionId;
  next();
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    version: '3.1-audit-grade',
    safety: safetyMonitor.getSystemState()
  });
});

// Arming endpoint
app.post('/api/arm', (req, res) => {
  const { activation_hash } = req.body;
  const result = sessionManager.armSession(req.sessionId, activation_hash);
  res.json(result);
});

// Coherence con safety monitor
app.post('/api/coherence/measure', async (req, res) => {
  try {
    // Verificar sesión armada (opcional en dev)
    if (process.env.REQUIRE_ARMING === 'true' && !sessionManager.isArmed(req.sessionId)) {
      return res.status(403).json({ error: 'System not armed' });
    }

    const response = await fetch(`${KERNEL_URL}/api/coherence/measure`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': req.headers['authorization'] || 'Bearer SERVICE_TOKEN_ENHANCED'
      },
      body: JSON.stringify({
        ...req.body,
        session_id: req.sessionId
      })
    });

    const coherence = await response.json();

    // GATE E: Safety Monitor
    const safetyCheck = safetyMonitor.checkCoherence(coherence, coherence.trace_id || req.sessionId);

    if (safetyCheck.action === 'BLOCK') {
      return res.status(400).json({
        error: 'Response blocked by safety monitor',
        reason: safetyCheck.reason,
        severity: safetyCheck.severity,
        trace_id: coherence.trace_id || req.sessionId
      });
    }

    res.json({
      ...coherence,
      safety_check: safetyCheck
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// System state
app.get('/api/system/state', (req, res) => {
  const session = sessionManager.getSession(req.sessionId);
  res.json({
    session: {
      id: req.sessionId,
      state: session?.state || 'UNKNOWN',
      armed: session?.armed || false
    },
    safety: safetyMonitor.getSystemState()
  });
});

// Timeout checker
setInterval(() => sessionManager.checkTimeout(), 60000);

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`✅ Backend Enhanced on ${PORT} (Hardened v3.1)`));
