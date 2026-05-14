import os
from flask import Flask, send_from_directory, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Developer: Lohitha Sai
# Setting up the main server logic
load_dotenv()

# Folders lekunda direct ga same directory nunchi files serve cheyyadaniki
app = Flask(__name__, static_folder='.', static_url_path='')

# Initializing OpenAI client for the study bot
client = OpenAI(api_key=os.environ.get("API_KEY"))

@app.route("/")
def lohitha_home():
    """Renders the main chat interface directly from the root folder."""
    print("Lohitha's AI assistant is running...") # Terminal lo kanipisthundi
    return send_from_directory('.', 'index.html')

@app.route("/chat", methods=["POST"])
def chat_with_bot():
    """Handles user inputs."""
    lohitha_user_msg = request.json.get("message")
    
    if not lohitha_user_msg:
        return jsonify({"error": "Message is empty. Try again!"}), 400

    try:
        # Calling OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI study assistant."},
                {"role": "user", "content": lohitha_user_msg}
            ]
        )
        
        bot_reply = response.choices[0].message.content
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        # Ekkadaina thappu jarigithe ee error print avtundi
        print(f"API connect avvatledu, Error: {e}")
        return jsonify({"error": "Server error. Check API connection."}), 500

if __name__ == "__main__":
    app.run(debug=True)
