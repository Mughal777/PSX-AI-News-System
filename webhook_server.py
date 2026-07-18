"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.2
webhook_server.py
=========================================================
TradingView Webhook Receiver
"""

from flask import Flask, request, jsonify
from datetime import datetime

from signal_manager import save_signal, load_signal, validate

app = Flask(__name__)

# ==========================================================
# LAST SIGNAL
# ==========================================================
# NOTE: last_signal ab sirf is process ki memory mein rehta hai.
# main.py alag process hai, is liye asal signal signal_manager.py
# ke zariye last_signal.json file mein save/load hota hai — yehi
# file main.py aur combined_signal.py padhte hain.

last_signal = None


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return "PSX AI Webhook Server Running"


# ==========================================================
# WEBHOOK
# ==========================================================

@app.route("/webhook", methods=["POST"])
def webhook():

    global last_signal

    data = request.json

    if not data:

        return jsonify(
            {
                "status": "error",
                "message": "No JSON received"
            }
        ), 400

    last_signal = data

    print()

    print("=" * 70)

    print("TRADINGVIEW ALERT RECEIVED")

    print("=" * 70)

    print("Time :", datetime.now())

    print()

    for key, value in data.items():

        print(f"{key:15} : {value}")

    print("=" * 70)

    # ہارڈ ڈسک پر محفوظ کریں تاکہ main.py (الگ پروسیس) اسے پڑھ سکے
    if validate(data):
        save_signal(data)
    else:
        print("[WARN]: Signal missing required fields (symbol/signal/score) — file not updated")

    return jsonify(
        {
            "status": "success"
        }
    )


# ==========================================================
# GET LAST SIGNAL
# ==========================================================

def get_last_signal():
    """پہلے in-memory signal، ورنہ ڈسک سے آخری محفوظ شدہ signal لوڈ کرتا ہے"""
    if last_signal is not None:
        return last_signal
    return load_signal()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print()

    print("=" * 70)

    print("PSX AI WEBHOOK SERVER STARTED")

    print("Listening : http://127.0.0.1:5000/webhook")

    print("=" * 70)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )