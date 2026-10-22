import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_ORIGIN", "*")}})

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

@app.get("/")
def home():
    return jsonify({
        "service": "Alstone Hauly AI API",
        "status": "running",
        "endpoints": ["/health", "/api/chat"]
    })

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "alstone-hauly-ai-backend"})

@app.post("/api/chat")
def chat():
    if not client:
        return jsonify({"error": "Server is missing OPENAI_API_KEY."}), 503

    data = request.get_json(silent=True) or {}
    message = data.get("message")
    history = data.get("history", [])

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Send a non-empty 'message' string."}), 400
    if not isinstance(history, list):
        return jsonify({"error": "'history' must be a list of messages."}), 400

    # Accept only a small, safe history format from the client.
    safe_history = []
    for item in history[-12:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and isinstance(content, str):
            safe_history.append({"role": role, "content": content[:4000]})

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are Hauly Tutor, a helpful AI assistant for learning, programming, and general questions. Explain clearly and safely."},
                *safe_history,
                {"role": "user", "content": message.strip()[:8000]}
            ],
        )
        reply = response.choices[0].message.content or ""
        return jsonify({"reply": reply, "model": OPENAI_MODEL})
    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({"error": "AI request failed. Check the backend logs and API configuration."}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
