import os
import requests
from flask import Flask, request
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "پروژه Flask شما با موفقیت و به صورت حرفه‌ای اجرا شد."

TELEGRAM_TOKEN = "8148296983:AAGeL81w9_RhAf4AsAlywE_YiGx0nE_aksY"
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
BOT_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "سلام دنیا"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        user_message = data["message"]["text"]

        gpt_reply = ask_groq_gpt(user_message)
        send_message(chat_id, gpt_reply)

    return "ok"

def ask_groq_gpt(message):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "شما یک دستیار حرفه‌ای هستید که با زبان‌های فارسی، عربی و انگلیسی به‌صورت طبیعی، محترمانه و روان پاسخ می‌دهید."},
            {"role": "user", "content": message}
        ]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return "در پردازش درخواست مشکلی پیش آمد."

def send_message(chat_id, text):
    url = f"{BOT_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
