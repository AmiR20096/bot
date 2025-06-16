from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "پروژه Flask شما با موفقیت و به صورت حرفه‌ای اجرا شد."
