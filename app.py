import os
import requests
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Ollama Setup
api_key = os.getenv("OLLAMA_API_KEY")  # Make sure this is set in Vercel
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# Ollama Cloud API endpoint
OLLAMA_API_URL = "https://api.ollama.com/v1/chat/completions"  # Chat completion endpoint

# Load Knowledge Base
kb_path = "knowledge_base.md"
try:
    with open(kb_path, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except Exception as e:
    KNOWLEDGE_BASE = "Dunes International School information: Timings 7:30 AM - 2:50 PM."

def ai_generate_answer(question, context):
    if not api_key:
        return "System Error: Ollama API Key missing."

    system_instruction = f"""
    You are ChatDIS, the official and friendly AI assistant for Dunes International School (DIS), Abu Dhabi.
    
    GUIDELINES:
    1. Use the PROVIDED CONTEXT below to answer the user's question accurately.
    2. If the answer is in the context, be specific (mention timings, dates, and contact info).
    3. If the answer is NOT in the context, politely state that you don't have that specific information and suggest they contact the school office at +971 2 552 7527.
    4. Keep the tone professional, welcoming, and helpful.
    5. Use bullet points for lists and bold text for important details.

    SCHOOL CONTEXT:
    {context}
    """

    try:
        response = requests.post(
            url="https://api.ollama.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gemini-3-flash-preview",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": question}
                ],
                "temperature": 0.5
            }
        )

        if response.status_code != 200:
            return f"API Error {response.status_code}: {response.text}"

        try:
            result = response.json()
        except ValueError:
            # Failed to parse JSON, return raw response for debugging
            return f"Raw response: {response.text}"

        if isinstance(result, dict):
            if "completion" in result:
                return result["completion"]
            elif "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("message", {}).get("content", "No content returned")
        
        return f"Unexpected API response: {result}"

    except Exception as e:
        return f"Connection Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").strip()
    # Pass the full KNOWLEDGE_BASE as context
    answer = ai_generate_answer(user_question, KNOWLEDGE_BASE)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run()
