from flask import Flask, request, jsonify

app = Flask(__name__)

ADMIN_API_KEY = "your-admin-key"
DAILY_LIMIT = 40
user_message_count = {}

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

    if api_key == ADMIN_API_KEY:
        pass
    else:
        count = user_message_count.get(user, 0)
        if count >= DAILY_LIMIT:
            return jsonify({"error": "Daily limit reached"}), 403
        user_message_count[user] = count + 1

    return jsonify({"reply": f"You said: {message}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
