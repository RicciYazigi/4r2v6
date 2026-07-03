import requests
import uuid
import time

AGW_URL = "http://localhost:8100"
AGW_API_KEY = "dummy_key"
CLIENT_ID = "chatbot_abc"

def precheck_llm_response(payload: dict, mode: str = "shadow") -> dict:
    trace_id = f"CHAT_{uuid.uuid4().hex[:6]}"
    body = {
        "node_id": "llm_response",
        "trace_id": trace_id,
        "payload": payload,
        "context": {"user_id": payload.get("user_id", "unknown")},
        "mode": mode
    }
    try:
        resp = requests.post(
            f"{AGW_URL}/analyze/{CLIENT_ID}",
            headers={"X-API-Key": AGW_API_KEY},
            json=body,
            timeout=5.0
        )
        if resp.status_code != 200:
            return {"decision": "escalate", "reasons": [{"message": f"Error API: {resp.status_code}"}], "meta": {}}
        return resp.json()
    except Exception as e:
        return {"decision": "escalate", "reasons": [{"message": f"Fallback por error: {str(e)}"}], "meta": {}}

def generate_llm_response(user_id: str, user_message: str):
    print(f"\n[BACKEND] Procesando Chat para: {user_id}")
    print(f"[BACKEND] Prompt: {user_message}")
    
    # 1. Simulación de LLM Draft
    draft_text = "¡Hola! Estoy aquí para ayudarte."
    if "consejos medicos" in user_message.lower():
        draft_text = "Deberías tomar 500mg de X medicamento."
    
    payload = {
        "user_id": user_id,
        "prompt": user_message,
        "response": draft_text,
        "response_tokens": len(draft_text.split()),
        "intent": "medical_advice" if "medico" in user_message.lower() else "general",
        "intent_risk_score": 0.8 if "medico" in user_message.lower() else 0.1,
        "sensitive_topic_score": 0.9 if "medico" in user_message.lower() else 0.05
    }

    # 2. Pre-check (SHADOW -> SOFT transition)
    # Forzamos 'soft' para el piloto 2
    decision_data = precheck_llm_response(payload, mode="soft")
    
    d = decision_data["decision"]
    reasons = [r["message"] for r in decision_data.get("reasons", [])]
    scores = decision_data.get("scores", {})
    coherence = scores.get("coherence_total", "ND")

    print(f"[ANTIGRAVITY] Veredicto: {d.upper()} (Coherencia: {coherence})")
    print(f"[ANTIGRAVITY] Razones: {reasons}")

    if d == "stop":
        print("[CHAT] BLOQUEADO: 'Lo siento, no puedo procesar esa solicitud por políticas de seguridad.'")
    elif d == "escalate":
        print("[CHAT] PENDIENTE: 'Un agente humano revisará tu consulta en breve.'")
    elif d == "degrade":
        print("[CHAT] DEGRADADO: 'Soy un asistente virtual, no puedo dar consejos médicos. Consulta a un profesional.'")
    else:
        print(f"[CHAT] OK: '{draft_text}'")

if __name__ == "__main__":
    # Simular un par de conversaciones
    # Caso 1: Seguro
    generate_llm_response("user_001", "Hola, ¿cómo estás?")
    time.sleep(1)
    # Caso 2: Sensible
    generate_llm_response("user_002", "Dame consejos medicos para el dolor")
