import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# AI Setup
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Load Knowledge Base safely
base_path = os.path.dirname(__file__)
kb_path = os.path.join(base_path, "..", "knowledge_base.md")
try:
    with open(kb_path, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except:
    KNOWLEDGE_BASE = "Error: Knowledge base file not found."

def search_knowledge_base(query):
    keywords = query.lower().split()
    relevant_lines = [line for line in KNOWLEDGE_BASE.split("\n") 
                      if any(word in line.lower() for word in keywords)]
    return "\n".join(relevant_lines[:15])

def ai_generate_answer(question, context):
    if not api_key:
        return "System Error: API Key missing."
    try:
        # UPDATED MODEL NAME HERE
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        You are ChatDIS, the assistant for Dunes International School.
        
        CONTEXT FROM SCHOOL FILES:
        {context}
        
        USER QUESTION:
        {question}
        
        INSTRUCTIONS:
        1. Use the context above to answer. 
        2. If the answer isn't there, use your general knowledge about schools but mention it's a general guess.
        3. Keep it friendly and 'Dunes' focused!
        """
        
        response = model.generate_content(prompt)
        return response.text
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        prompt = f"Using this info: {context}. Answer this: {question}. Be a helpful Dunes School assistant."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}" # This will tell us EXACTLY why it's failing

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").strip()
    relevant_info = search_knowledge_base(user_question)
    
    # If search fails to find anything in the .md file
    if not relevant_info.strip():
        return jsonify({"answer": "I couldn't find specific details on that. Please ask the school office!"})

    answer = ai_generate_answer(user_question, relevant_info)
    return jsonify({"answer": answer})

# Vercel will look for this 'app' variable
app = app
