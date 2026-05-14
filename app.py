import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# initialize client for lohitha's project
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_bot():
    req_data = request.get_json()
    msg = req_data.get("message")
    
    if not msg:
        return jsonify({"error": "empty message"}), 400

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a smart AI study assistant. Help the user clear their doubts briefly and accurately."},
                {"role": "user", "content": msg}
            ]
        )
        bot_reply = completion.choices[0].message.content
        return jsonify({"reply": bot_reply})
    
    except Exception as e:
        # logging error to console
        print(f"Error: {e}") 
        return jsonify({"error": "something went wrong"}), 500

if __name__ == '__main__':
    app.run(debug=True)
