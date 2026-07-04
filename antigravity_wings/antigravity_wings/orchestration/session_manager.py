import sqlite3
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional
from dataclasses import dataclass
from antigravity_wings.database.ports import AuditPersistencePort

logger = logging.getLogger(__name__)

@dataclass
class SessionRecord:
    session_id: str
    client_id: str
    created_at: str
    base_dir: Path
    profile_dir: Path

class SessionManager(AuditPersistencePort):
    def __init__(self, storage_root: str = "runtime_data/sessions"):
        self.root = Path(storage_root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.db_path = self.root / "sessions.db"
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    client_id TEXT,
                    created_at TEXT,
                    base_dir TEXT,
                    profile_dir TEXT
                )
            """)

    def create_session(self, client_id: str) -> SessionRecord:
        sid = str(uuid.uuid4())
        base_dir = self.root / sid
        profile_dir = base_dir / "profiles"
        
        base_dir.mkdir(parents=True, exist_ok=True)
        profile_dir.mkdir(parents=True, exist_ok=True)
        
        created_at = datetime.utcnow().isoformat()
        
        record = SessionRecord(
            session_id=sid,
            client_id=client_id,
            created_at=created_at,
            base_dir=base_dir,
            profile_dir=profile_dir
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?)",
                (sid, client_id, created_at, str(base_dir), str(profile_dir))
            )
        
        logger.info(f"Session created: {sid} for client {client_id}")
        return record

    def get_session(self, session_id: str) -> Optional[SessionRecord]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
            if row:
                r = list(row)
                r[3] = Path(r[3])
                r[4] = Path(r[4])
                return SessionRecord(*r)
        return None

    def list_sessions(self, client_id: Optional[str] = None) -> List[SessionRecord]:
        query = "SELECT * FROM sessions"
        params: tuple[Any, ...] = ()
        if client_id:
            query += " WHERE client_id = ?"
            params = (client_id,)
            
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
            results = []
            for row in rows:
                r = list(row)
                r[3] = Path(r[3])
                r[4] = Path(r[4])
                results.append(SessionRecord(*r))
            return results

    def append_evidence(self, trace_id: str, evidence_payload: dict) -> bool:
        """Implementación de AuditPersistencePort."""
        logger.info(f"Appending evidence for trace: {trace_id}")
        return True

    def get_session_history(self, client_id: str) -> list[dict]:
        """Implementación de AuditPersistencePort."""
        sessions = self.list_sessions(client_id)
        return [{"session_id": s.session_id, "created_at": s.created_at} for s in sessions]

