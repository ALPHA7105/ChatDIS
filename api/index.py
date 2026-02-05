from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))

app = Flask(__name__)

# Load knowledge base
with open("knowledge_base.md", "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE = f.read()

def search_knowledge_base(query):
    keywords = query.lower().split()
    relevant_lines = []
    for line in KNOWLEDGE_BASE.split("\n"):
        for word in keywords:
            if word in line.lower():
                relevant_lines.append(line)
                break
    return "\n".join(relevant_lines[:15])

def ai_generate_answer(question, context):
    """
    This function sends the prompt to the real Gemini AI.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # We give the AI a "Persona" so it knows it's at Dunes
        prompt = f"""
        You are ChatDIS, the official digital assistant for Dunes International School. 
        Use the following verified school information to answer the user's question.
        
        SCHOOL INFORMATION:
        {context}
        
        USER QUESTION: 
        {question}
        
        INSTRUCTIONS:
        - Be polite, professional, and welcoming.
        - Use "Dunes International School" context.
        - If the information is not in the context, politely say you don't know and suggest contacting the school office.
        - Keep the answer concise.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"AI Error: {e}")
        return "I'm having trouble thinking right now. Please check back in a moment or contact the school office."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "").strip()
    if not user_question:
        return jsonify({"answer": "Please enter a question."})
    relevant_info = search_knowledge_base(user_question)
    if not relevant_info.strip():
        return jsonify({"answer": "I don’t have that information. Please contact the school office."})
    answer = ai_generate_answer(user_question, relevant_info)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    print("--- ChatDIS Server Starting ---")
    print("Go to http://127.0.0.1:5000 in your browser")
    app.run(debug=True)


if __name__ == "__main__":
    app.run()
