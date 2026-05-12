from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

def bot_reply(message):

    msg = message.lower()

    replies = {
        "hi": "Hello 👋",
        "hello": "Hi, how can I help you?",
        "python": "Python is a powerful programming language.",
        "html": "HTML is used to create web pages.",
        "css": "CSS is used for styling websites.",
        "ai": "AI stands for Artificial Intelligence.",
        "machine learning": "Machine Learning allows systems to learn from data.",
        "bye": "Goodbye 👋"
    }

    for key in replies:
        if key in msg:
            return replies[key]

    return "Sorry, I don't understand that yet."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    bot_message = bot_reply(user_message)

    current_time = datetime.now().strftime("%H:%M")

    return jsonify({
        "reply": bot_message,
        "time": current_time
    })

if __name__ == "__main__":
    app.run(debug=True)
