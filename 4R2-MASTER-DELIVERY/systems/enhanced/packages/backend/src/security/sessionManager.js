/**
 * Session Manager - Manejo de sesiones con arming protocol
 */
export class SessionManager {
  constructor() {
    this.sessions = new Map();
    this.TIMEOUT_MS = 30 * 60 * 1000; // 30 min
  }

  createSession(sessionId) {
    const session = {
      id: sessionId,
      armed: false,
      createdAt: Date.now(),
      lastActivity: Date.now(),
      state: 'LOCKED'
    };
    this.sessions.set(sessionId, session);
    return session;
  }

  armSession(sessionId, activationHash) {
    const session = this.sessions.get(sessionId);
    if (!session) return { success: false, error: 'Session not found' };
    
    const expected = process.env.ACTIVATION_HASH;
    if (!expected) {
      throw new Error("FATAL: ACTIVATION_HASH not set");
    }

    const crypto = require('node:crypto');
    const a = Buffer.from(String(activationHash));
    const b = Buffer.from(expected);
    
    const ok = a.length === b.length && crypto.timingSafeEqual(a, b);
    if (!ok) {
      return { success: false, error: 'Invalid activation hash' };
    }
    
    session.armed = true;
    session.state = 'ARMED';
    session.lastActivity = Date.now();
    
    return { success: true, session };
  }

  checkTimeout() {
    const now = Date.now();
    for (const [id, session] of this.sessions) {
      if (session.armed && (now - session.lastActivity) > this.TIMEOUT_MS) {
        session.armed = false;
        session.state = 'TIMEOUT';
        console.log(`[SessionManager] Timeout: ${id}`);
      }
    }
  }

  getSession(sessionId) {
    return this.sessions.get(sessionId);
  }

  isArmed(sessionId) {
    const session = this.sessions.get(sessionId);
    return session?.armed || false;
  }
}
