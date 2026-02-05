import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)

# AI Setup
api_key = os.getenv("API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("CRITICAL: No API Key found!")

# 1. FIX: Updated path for knowledge_base.md in root folder
kb_path = "knowledge_base.md"
try:
    with open(kb_path, "r", encoding="utf-8") as f:
        KNOWLEDGE_BASE = f.read()
except Exception as e:
    print(f"File Error: {e}")
    KNOWLEDGE_BASE = "Dunes International School information: Timings 7:45 AM - 2:50 PM."

def search_knowledge_base(query):
    keywords = query.lower().split()
    relevant_lines = [line for line in KNOWLEDGE_BASE.split("\n") 
                      if any(word in line.lower() for word in keywords)]
    return "\n".join(relevant_lines[:15])
"""
def ai_generate_answer(question, context):
    if not api_key:
        return "System Error: API Key missing in Vercel settings."
    try:
        # Using the standard stable name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f
        You are ChatDIS, the official assistant for Dunes International School.
        
        CONTEXT:
        {context}
        
        USER QUESTION:
        {question}
        
        INSTRUCTIONS:
        1. Answer based on the context.
        2. Be polite and professional.
        
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # If 1.5-flash still fails, try the older stable pro model as a backup
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except:
            return f"AI Error: {str(e)}"
"""
def ai_generate_answer(question, context):
    model = genai.GenerativeModel('gemini-2.5-flash')
    try:
        # Just a simple test
        response = model.generate_content(f"You are a school assistant. {question}")
        return response.text
    except Exception as e:
        return f"Still Error: {str(e)}"
        
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").strip()
    relevant_info = search_knowledge_base(user_question)
    
    # If search finds nothing, we still let the AI try to answer 
    # but tell it the context is empty
    if not relevant_info.strip():
        relevant_info = "No specific school document found for this query."

    answer = ai_generate_answer(user_question, relevant_info)
    return jsonify({"answer": answer})

# Vercel entry point
if __name__ == "__main__":
    app.run()
