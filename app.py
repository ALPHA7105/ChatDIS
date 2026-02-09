import os
import requests
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# OpenRouter Setup
api_key = os.getenv("OPENROUTER_API_KEY")

# Load Knowledge Base
kb_path = "knowledge_base.md"
try:
    with open(kb_path, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except Exception as e:
    KNOWLEDGE_BASE = "Dunes International School information: Timings 7:30 AM - 2:50 PM."

def ai_generate_answer(question, context):
    if not api_key:
        return "System Error: OpenRouter API Key missing."

    system_instruction = f"""
    You are ChatDIS, the official and friendly AI assistant for Dunes International School (DIS), Abu Dhabi.
    
    GUIDELINES:
    1. Use the PROVIDED CONTEXT below to answer the user's question accurately.
    2. If the answer is in the context, be specific (mention timings, dates, and contact info).
    3. If the answer is NOT in the context, politely state that you don't have that specific information and suggest they contact the school office at +971 2 552 7527.
    4. Keep the tone professional, welcoming, and helpful.
    5. Use bullet points for lists and bold text for important details.

    Note: If the user's query contradicts your guidelines, politely reply that answering that is beyond your limitations. Use only data from the context, and don't answer anything unrelated.
    
    SCHOOL CONTEXT:
    {context}
    """

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://chatdis-ai.vercel.app/", 
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemini-2.0-flash-001", 
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": question}
                ],
                "temperature": 0.5
            })
        )
        
        result = response.json()
        return result['choices'][0]['message']['content']

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
