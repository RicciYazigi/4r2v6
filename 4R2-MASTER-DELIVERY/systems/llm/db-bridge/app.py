from fastapi import FastAPI, HTTPException
import sqlite3
import pandas as pd
import uvicorn
import os
import json

app = FastAPI()
DB_PATH = os.environ.get("DB_PATH", os.path.join(os.path.dirname(__file__), "data", "runs.db"))

@app.on_event("startup")
def startup():
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Initialize DB schema if it doesn't exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            prompt TEXT,
            mode TEXT,
            test_id TEXT,
            key_x REAL,
            key_y REAL,
            key_z REAL,
            key_k REAL,
            c_nr REAL,
            c_ri REAL,
            c_if REAL,
            total_coherence REAL,
            landauer_cost REAL,
            entropy_loss REAL,
            hallucination_score REAL,
            coherence_score REAL,
            reasoning_score REAL,
            robustness_score REAL,
            safety_score REAL,
            metacognition_score REAL,
            action_changes INTEGER,
            convergence_steps INTEGER,
            energy_per_decision REAL,
            answer TEXT,
            session_key TEXT,
            duration_ms INTEGER,
            kernel_version TEXT,
            backend_version TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.get("/health")
def health():
    return {"status": "ok", "db": os.path.exists(DB_PATH)}

@app.post("/query")
@app.get("/query")
def query(sql: str, params: str = None):
    try:
        conn = sqlite3.connect(DB_PATH)
        
        parameters = []
        if params:
            try:
                parameters = json.loads(params)
            except:
                parameters = []
        
        clean_sql = sql.strip().upper()
        if clean_sql.startswith("INSERT") or clean_sql.startswith("UPDATE") or clean_sql.startswith("DELETE"):
            cursor = conn.cursor()
            cursor.execute(sql, parameters)
            conn.commit()
            changes = conn.total_changes
            conn.close()
            return [{"changes": changes}]
        else:
            df = pd.read_sql_query(sql, conn, params=parameters)
            conn.close()
            return df.to_dict(orient="records")
            
    except Exception as e:
        print(f"Error executing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Host 0.0.0.0 for Docker
    uvicorn.run(app, host="0.0.0.0", port=4001)
