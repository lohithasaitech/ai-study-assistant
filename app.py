import os
import requests
from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv

# App setup by Lohitha Sai
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# Loading credentials from .env
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

@app.route("/")
def render_home():
    return send_from_directory('.', 'index.html')

@app.route("/chat", methods=["POST"])
def chat_logic():
    user_text = request.json.get("message")
    
    if not user_text:
        return jsonify({"error": "Empty text received"}), 400

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a study assistant created by Lohitha Sai. Be helpful and concise."
                },
                {"role": "user", "content": user_text}
            ]
        }
        
        req = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        data = req.json()
        
        reply_msg = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply_msg})
        
    except Exception as e:
        print("Backend Error:", e)
        return jsonify({"error": "Server issue. Please try again."}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
