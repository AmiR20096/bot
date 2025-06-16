import telebot
import requests
from flask import Flask, request

TELEGRAM_BOT_TOKEN = "7139419433:AAG4AI-RuJqqTsgExQk5NXjsh5FHEF42hLs"
GROQ_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

def detect_language(text):
    if any(c in text for c in "ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدپو"):
        return "fa"
    elif any(c in text for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"):
        return "ar"
    else:
        return "en"

def ask_groq(question):
    language = detect_language(question)
    system_prompt = {
        "fa": "شما یک دستیار فارسی‌زبان هستی. با لحن حرفه‌ای و طبیعی پاسخ بده.",
        "ar": "أنت مساعد ذكي يتحدث اللغة العربية. أجب بلغة طبيعية وودية.",
        "en": "You are a helpful AI assistant. Respond naturally and professionally."
    }[language]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    }

    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
        else:
            return "❌ خطا در پاسخ از هوش مصنوعی."
    except:
        return "⚠️ اتصال به سرور با خطا مواجه شد."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    reply = ask_groq(message.text)
    bot.reply_to(message, reply)

@app.route('/')
def home():
    return 'Vixa bot is running.'

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url='https://vixa-bot.onrender.com/7139419433:AAG4AI-RuJqqTsgExQk5NXjsh5FHEF42hLs')  # آدرس واقعی Render رو جایگزین کن
    app.run(host='0.0.0.0', port=8080)
