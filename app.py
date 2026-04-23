import os
import json
from groq import Groq
from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from datetime import datetime

load_dotenv()

app = Flask(__name__)

CORS(app)

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

KB_PATH = "knowledge_base.md"
try:
    with open(KB_PATH, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except Exception:
    KNOWLEDGE_BASE = "Dunes International School info: Timings 7:30 AM - 2:50 PM."


def build_system_instruction(context):
    return f"""You are ChatDIS, the official and friendly AI assistant for Dunes International School (DIS), Abu Dhabi.

GUIDELINES:
1. Use the PROVIDED CONTEXT below to answer the user's question accurately.
2. If the answer is in the context, be specific (mention timings, dates, and contact info).
3. If the answer is NOT in the context, politely state that you don't have that specific information and suggest contacting the school office at +971 2 552 7527.
4. Keep the tone professional, welcoming, and helpful.
5. Use bullet points for lists and bold text for important details.

SCHOOL CONTEXT:
{context}"""


def build_messages(question, context):
    return [
        {"role": "system", "content": build_system_instruction(context)},
        {"role": "user", "content": question}
    ]


def ai_generate_answer(question, context):
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=build_messages(question, context),
            temperature=0.5,
            max_completion_tokens=8192,
            top_p=1,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Connection Error: {str(e)}"


def ai_generate_stream(question, context):
    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=build_messages(question, context),
            temperature=0.5,
            max_completion_tokens=8192,
            top_p=1,
            stream=True
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield "data: " + json.dumps({"token": content}) + "\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield "data: " + json.dumps({"error": f"Connection Error: {str(e)}"}) + "\n\n"


def log_prompt(user_question, client_ip):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {client_ip} | {user_question}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/widget")
def widget():
    return render_template("widget.html")


@app.route("/ask", methods=["POST"])
@limiter.limit("5 per minute")
def ask():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    user_question = data.get("question", "").strip()
    client_ip = request.remote_addr

    if not user_question or len(user_question) > 1000:
        return jsonify({"error": "Invalid question"}), 400

    log_prompt(user_question, client_ip)

    answer = ai_generate_answer(user_question, KNOWLEDGE_BASE)
    return jsonify({"answer": answer})


@app.route("/ask/stream", methods=["POST"])
@limiter.limit("5 per minute")
def ask_stream():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    user_question = data.get("question", "").strip()
    client_ip = request.remote_addr

    if not user_question or len(user_question) > 1000:
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
