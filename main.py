import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "7139419433:AAG4AI-RuJqqTsgExQk5NXjsh5FHEF42hLs"
GROQ_API_KEY = "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"

BOT_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def home():
    return 'ربات با موفقیت فعال است.'

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        reply = ask_groq(text)
        send_reply(chat_id, reply)

    return "ok"

def ask_groq(message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "شما یک دستیار هوشمند هستید که به صورت طبیعی و حرفه‌ای به زبان فارسی، عربی و انگلیسی پاسخ می‌دهید."},
            {"role": "user", "content": message}
        ]
    }

    try:
        res = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        else:
            return "در پردازش پاسخ مشکلی پیش آمد."
    except:
        return "خطا در اتصال به مدل هوش مصنوعی."

def send_reply(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(f"{BOT_API_URL}/sendMessage", json=payload)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
