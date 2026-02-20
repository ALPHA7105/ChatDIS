"""
import os
import requests
from flask import Flask, request, jsonify, render_template, abort
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Rate limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# Ollama Cloud setup
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
CHATDIS_SECRET_KEY = os.getenv("CHATDIS_SECRET_KEY")

OLLAMA_API_URL = "https://ollama.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json"
}

# Load knowledge base
KB_PATH = "knowledge_base.md"
try:
    with open(KB_PATH, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except Exception:
    KNOWLEDGE_BASE = "Dunes International School info: Timings 7:30 AM - 2:50 PM."


def ai_generate_answer(question, context):
    if not OLLAMA_API_KEY:
        return "System Error: Ollama API Key is missing."

    system_instruction = f"""
You are ChatDIS, the official and friendly AI assistant for Dunes International School (DIS), Abu Dhabi.

SCHOOL CONTEXT:
{context}
"""

    payload = {
        "model": "gemini-3-flash-preview",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": question}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=HEADERS, json=payload)
        if response.status_code != 200:
            return f"API Error {response.status_code}: {response.text}"

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]

        return "Unexpected API response."

    except Exception as e:
        return f"Connection Error: {str(e)}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
@limiter.limit("5 per minute")
def ask():
    # 🔐 Check API key from CLIENT request
    client_key = request.headers.get("x-api-key")

    if client_key != CHATDIS_SECRET_KEY:
        abort(401)

    user_question = request.json.get("question", "").strip()

    if not user_question or len(user_question) > 1000:
        return jsonify({"error": "Invalid question"}), 400

    answer = ai_generate_answer(user_question, KNOWLEDGE_BASE)
    return jsonify({"answer": answer})


if __name__ == "__main__":
    app.run(debug=False)

"""











import os
import requests
from flask import Flask, request, jsonify, render_template, abort
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Rate limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

# Ollama Cloud setup
API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_API_URL = "https://ollama.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    "x-api-key": "super_secure_school_key_123"
}

# Load knowledge base
KB_PATH = "knowledge_base.md"
try:
    with open(KB_PATH, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except Exception:
    KNOWLEDGE_BASE = "Dunes International School info: Timings 7:30 AM - 2:50 PM."

def ai_generate_answer(question, context):
    if not API_KEY:
        return "System Error: Ollama API Key is missing."

    system_instruction = f"""
You are ChatDIS, the official and friendly AI assistant for Dunes International School (DIS), Abu Dhabi.

GUIDELINES:
1. Use the PROVIDED CONTEXT below to answer the user's question accurately.
2. If the answer is in the context, be specific (mention timings, dates, and contact info).
3. If the answer is NOT in the context, politely state that you don't have that specific information and suggest contacting the school office at +971 2 552 7527.
4. Keep the tone professional, welcoming, and helpful.
5. Use bullet points for lists and bold text for important details.

SCHOOL CONTEXT:
{context}
"""

    payload = {
        "model": "gemini-3-flash-preview",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": question}
        ],
        "temperature": 0.5
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=HEADERS, json=payload)
        if response.status_code != 200:
            return f"API Error {response.status_code}: {response.text}"

        result = response.json()

        # Ollama Cloud returns choices -> message -> content
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0].get("message", {}).get("content", "No content returned")

        return f"Unexpected API response: {result}"

    except Exception as e:
        return f"Connection Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")
""
@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").strip()
    answer = ai_generate_answer(user_question, KNOWLEDGE_BASE)
    return jsonify({"answer": answer})
""
@app.route("/ask", methods=["POST"])
@limiter.limit("5 per minute")
def ask():
    # Check API key from request header
    client_key = request.headers.get("x-api-key")
    server_key = os.getenv("CHATDIS_SECRET_KEY")

    if client_key != server_key:
        abort(401)  # Unauthorized

    user_question = request.json.get("question", "").strip()
    answer = ai_generate_answer(user_question, KNOWLEDGE_BASE)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

