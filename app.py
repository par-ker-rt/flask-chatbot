from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

ADMIN_API_KEY = "ef1dd21d04c7162581dc9de9ebdb629f"
DAILY_LIMIT = 40
user_message_count = {}

def get_today():
    return datetime.utcnow().strftime("%Y-%m-%d")

@app.route("/")
def index():
    return "Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user = data.get("user")
    message = data.get("message")
    api_key = data.get("api_key")

    if not user or not message:
        return jsonify({"error": "Missing user or message"}), 400

    # Không giới hạn nếu là admin
    if api_key != ADMIN_API_KEY:
        today = get_today()
        if user not in user_message_count:
            user_message_count[user] = {}
        if today not in user_message_count[user]:
            user_message_count[user][today] = 0

        if user_message_count[user][today] >= DAILY_LIMIT:
            return jsonify({"error": "Daily message limit reached"}), 403

        user_message_count[user][today] += 1

    return jsonify({"reply": f"You said: {message}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
