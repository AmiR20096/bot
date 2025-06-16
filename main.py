from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = "7139419433:AAG4AI-RuJqqTsgExQk5NXjsh5FHEF42hLs"
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)
  
def get_groq_response(user_message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "شما یک ربات هوشمند هستید."},
            {"role": "user", "content": user_message}
        ]
    }
    response = requests.post(GROQ_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "خطا در دریافت پاسخ از هوش مصنوعی."

@app.route('/', methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"]["text"]
        reply = get_groq_response(user_text)
        send_message(chat_id, reply)
    return "ok"
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
