"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.2
signal_manager.py
=========================================================
TradingView Signal Manager
"""

import json
import os
from datetime import datetime

SIGNAL_FILE = "last_signal.json"


# ==========================================================
# SAVE SIGNAL
# ==========================================================

def save_signal(signal):

    signal["received_time"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        SIGNAL_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(

            signal,

            f,

            indent=4

        )


# ==========================================================
# LOAD SIGNAL
# ==========================================================

def load_signal():

    if not os.path.exists(SIGNAL_FILE):

        return None

    try:

        with open(

            SIGNAL_FILE,

            "r",

            encoding="utf-8"

        ) as f:

            return json.load(f)

    except:

        return None


# ==========================================================
# VALIDATE SIGNAL
# ==========================================================

def validate(signal):

    required = [

        "symbol",

        "signal",

        "score"

    ]

    for field in required:

        if field not in signal:

            return False

    return True


# ==========================================================
# PRINT SIGNAL
# ==========================================================

def print_signal(signal):

    if signal is None:

        print()

        print("No TradingView Signal")

        return

    print()

    print("="*60)

    print("LATEST TRADINGVIEW SIGNAL")

    print("="*60)

    for key,value in signal.items():

        print(f"{key:18} : {value}")

    print("="*60)


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample={

        "symbol":"OGDC",

        "signal":"BUY",

        "score":91,

        "rsi":63,

        "adx":29,

        "volume":"Strong"

    }

    save_signal(sample)

    s=load_signal()

    print_signal(s)