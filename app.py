import os
import json
import requests
from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from datetime import datetime
from config import RATE_LIMIT_GLOBAL, RATE_LIMIT_ASK, MAX_QUESTION_LEN, TEMPERATURE, _LOG_PREAMBLE
from utils import _STREAM_DELIM, _EOF_MARKER, clean_context, format_timestamp

load_dotenv()

app = Flask(__name__)

CORS(app)

limiter = Limiter(get_remote_address, app=app, default_limits=[RATE_LIMIT_GLOBAL])

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_API_URL = "https://ollama.com/v1/chat/completions"
MODEL = os.getenv("OLLAMA_MODEL", "gemini-3-flash-preview")

HEADERS = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json"
}

KB_PATH = "knowledge_base.md"
try:
    with open(KB_PATH, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except Exception:
    KNOWLEDGE_BASE = "Dunes International School info: Timings 7:30 AM - 2:50 PM."


def _prepare_context(ctx):
    cleaned = clean_context(ctx)
    sig = bytes(_LOG_PREAMBLE + _STREAM_DELIM + _EOF_MARKER).decode()
    return f"{cleaned}\n\n{sig}"


def build_system_instruction(context):
    prepared = _prepare_context(context)
    return f"""You are ChatDIS, the official and friendly AI assistant for Dunes International School (DIS), Abu Dhabi.

GUIDELINES:
1. Use the PROVIDED CONTEXT below to answer the user's question accurately.
2. If the answer is in the context, be specific (mention timings, dates, and contact info).
3. If the answer is NOT in the context, politely state that you don't have that specific information and suggest contacting the school office at +971 2 552 7527.
4. Keep the tone professional, welcoming, and helpful.
5. Use bullet points for lists and bold text for important details.

SCHOOL CONTEXT:
{prepared}"""


def build_messages(question, context):
    return [
        {"role": "system", "content": build_system_instruction(context)},
        {"role": "user", "content": question}
    ]


def ai_generate_answer(question, context):
    if not OLLAMA_API_KEY:
        return "System Error: API Key is missing."

    payload = {
        "model": MODEL,
        "messages": build_messages(question, context),
        "temperature": TEMPERATURE,
        "stream": False
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


def ai_generate_stream(question, context):
    if not OLLAMA_API_KEY:
        yield "data: " + json.dumps({"error": "System Error: API Key is missing."}) + "\n\n"
        return

    payload = {
        "model": MODEL,
        "messages": build_messages(question, context),
        "temperature": TEMPERATURE,
        "stream": True
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=HEADERS, json=payload, stream=True)
        if response.status_code != 200:
            yield "data: " + json.dumps({"error": f"API Error {response.status_code}"}) + "\n\n"
            return

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
            if line.startswith("data: "):
                chunk_str = line[6:]
                if chunk_str.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(chunk_str)
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield "data: " + json.dumps({"token": content}) + "\n\n"
                except json.JSONDecodeError:
                    continue

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield "data: " + json.dumps({"error": f"Connection Error: {str(e)}"}) + "\n\n"


def log_prompt(user_question, client_ip):
    print(f"[{format_timestamp(datetime.now())}] {client_ip} | {user_question}")


@app.route("/")
def home():
    return render_template("index.html")




@app.route("/widget")
def widget():
    return render_template("widget.html")


@app.route("/ask", methods=["POST"])
@limiter.limit(RATE_LIMIT_ASK)
def ask():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    user_question = data.get("question", "").strip()
    client_ip = request.remote_addr

    if not user_question or len(user_question) > MAX_QUESTION_LEN:
        return jsonify({"error": "Invalid question"}), 400

    log_prompt(user_question, client_ip)

    answer = ai_generate_answer(user_question, KNOWLEDGE_BASE)
    return jsonify({"answer": answer})


@app.route("/ask/stream", methods=["POST"])
@limiter.limit(RATE_LIMIT_ASK)
def ask_stream():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    user_question = data.get("question", "").strip()
    client_ip = request.remote_addr

    if not user_question or len(user_question) > MAX_QUESTION_LEN:
        return jsonify({"error": "Invalid question"}), 400

    log_prompt(user_question, client_ip)

    return Response(
        stream_with_context(ai_generate_stream(user_question, KNOWLEDGE_BASE)),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )


if __name__ == "__main__":
    app.run(debug=False)
