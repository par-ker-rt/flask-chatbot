from flask import Flask, request, jsonify, render_template
import os
import openai

app = Flask(__name__)

# Lấy biến môi trường từ Render
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "ef1dd21d04c7162581dc9de9ebdb629f")
DAILY_LIMIT = int(os.getenv("LIMIT_PER_DAY", 40))
openai.api_key = os.getenv("OPENAI_API_KEY")

# Biến lưu số lượng tin nhắn mỗi user mỗi ngày
user_message_count = {}

@app.route("/")
def index():
    return render_template("index.html")  # Trả về giao diện chatbot

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user = data.get("user")
    message = data.get("message")
    api_key = data.get("api_key")

    if not user or not message:
        return jsonify({"error": "Missing user or message"}), 400

    if api_key != ADMIN_API_KEY:
        count = user_message_count.get(user, 0)
        if count >= DAILY_LIMIT:
            return jsonify({"error": "Daily limit reached"}), 403
        user_message_count[user] = count + 1

    # Sử dụng API chuẩn mới của openai >=0.28.1
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # hoặc "gpt-4" nếu được cấp quyền
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
