"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.2
dashboard.py - COLOR TERMINAL UPGRADE
=========================================================
Professional Console Dashboard with ANSI Colors
"""

import os
from datetime import datetime

# ANSI Color Codes for Windows CMD / Linux Terminal
CLR_RESET = "\033[0m"
CLR_BOLD = "\033[1m"
CLR_GREEN = "\033[92m"
CLR_RED = "\033[91m"
CLR_YELLOW = "\033[93m"
CLR_CYAN = "\033[96m"
CLR_MAGENTA = "\033[95m"

# ==========================================================
# CLEAR SCREEN
# ==========================================================
def clear():
    """کنسول اسکرین کو صاف کرتا ہے"""
    os.system("cls" if os.name == "nt" else "clear")

# ==========================================================
# DASHBOARD DISPLAY ENGINE
# ==========================================================
def show_dashboard(result=None, news=None):
    """رن ٹائم پر خبروں کا خوبصورت اور کلر فل ڈیش بورڈ دکھاتا ہے"""
    clear()
    now = datetime.now()

    print(f"{CLR_CYAN}=" * 72)
    print(f"               {CLR_BOLD}PSX AI NEWS TERMINAL v2.2{CLR_RESET}{CLR_CYAN}")
    print(f"=" * 72 + CLR_RESET)

    print(f"{CLR_BOLD}Date :{CLR_RESET} {now.strftime('%d-%b-%Y')}  |  {CLR_BOLD}Time :{CLR_RESET} {now.strftime('%I:%M:%S %p')}")
    print(f"{CLR_CYAN}-" * 72 + CLR_RESET)

    if result is None:
        print(f"{CLR_BOLD}Status               :{CLR_RESET} {CLR_GREEN}Waiting For News...{CLR_RESET}")
        print(f"{CLR_BOLD}News Feed            :{CLR_RESET} Connected 🌐")
        print(f"{CLR_BOLD}AI Engine            :{CLR_RESET} Ready 🧠")
        print(f"{CLR_BOLD}Desktop Notification :{CLR_RESET} ACTIVE 🔔")
        print(f"{CLR_CYAN}-" * 72 + CLR_RESET)
        return

    # امپیکٹ اسکور کے حساب سے ہیڈ لائن کا رنگ متعین کریں
    impact = result.get("impact_score", 0)
    headline_color = CLR_YELLOW if impact >= 7 else CLR_BOLD
    
    print(f"{CLR_BOLD}Headline   :{CLR_RESET} {headline_color}{news['title']}{CLR_RESET}")
    print(f"{CLR_BOLD}Source     :{CLR_RESET} {news['source']}")
    
    # سینٹیمنٹ اور پرائیورٹی کا کلر کوڈ
    sentiment = result.get("sentiment", "neutral").lower()
    sent_color = CLR_GREEN if sentiment == "positive" else (CLR_RED if sentiment == "negative" else CLR_RESET)
    
    priority = result.get("priority", "LOW").upper()
    pri_color = CLR_RED if priority == "HIGH" else (CLR_YELLOW if priority == "MEDIUM" else CLR_RESET)

    print(f"{CLR_BOLD}Impact     :{CLR_RESET} {impact}/10")
    print(f"{CLR_BOLD}Priority   :{CLR_RESET} {pri_color}{priority}{CLR_RESET}")
    print(f"{CLR_BOLD}Sentiment  :{CLR_RESET} {sent_color}{sentiment.upper()}{CLR_RESET}")
    print(f"{CLR_BOLD}Confidence :{CLR_RESET} {result['confidence']}%")
    print(f"{CLR_CYAN}-" * 72 + CLR_RESET)

    # متاثرہ اسٹاکس
    stocks = result.get("affected_stocks", [])
    if stocks:
        print(f"{CLR_BOLD}Affected Stocks:{CLR_RESET}")
        for s in stocks:
            print(f"   • {CLR_YELLOW}{s}{CLR_RESET}")
    else:
        print(f"{CLR_BOLD}Affected Stocks :{CLR_RESET} None")

    print(f"{CLR_CYAN}-" * 72 + CLR_RESET)

    # متاثرہ سیکٹرز
    sectors = result.get("affected_sectors", [])
    if sectors:
        print(f"{CLR_BOLD}Affected Sectors:{CLR_RESET}")
        for s in sectors:
            print(f"   • {CLR_MAGENTA}{s}{CLR_RESET}")
    else:
        print(f"{CLR_BOLD}Affected Sectors :{CLR_RESET} None")

    print(f"{CLR_CYAN}-" * 72 + CLR_RESET)

    # جیوگرافی / ممالک
    geo = result.get("geo", [])
    if geo:
        print(f"{CLR_BOLD}Countries:{CLR_RESET}")
        for g in geo:
            print(f"   • {g}")
        print(f"{CLR_CYAN}-" * 72 + CLR_RESET)

    # اردو خلاصہ (AI Summary)
    print(f"{CLR_BOLD}AI Summary (Urdu):{CLR_RESET}")
    print(f"{CLR_GREEN}{result.get('reasoning_urdu', 'کوئی خلاصہ دستیاب نہیں ہے۔')}{CLR_RESET}")
    print(f"{CLR_CYAN}-" * 72 + CLR_RESET)

    # خبر کا لنک
    print(f"{CLR_BOLD}News Link:{CLR_RESET}")
    print(f"{CLR_CYAN}{news['link']}{CLR_RESET}")
    print(f"{CLR_CYAN}=" * 72 + CLR_RESET)


# ==========================================================
# MASTER (COMBINED) SIGNAL PANEL
# TradingView + News + Market Bias — teeno ko mila kar aik
# final panel, taake ek nazar mein pata chal jaye asal decision.
# ==========================================================
def show_combined_panel(combined):
    """combined_signal.get_combined_signal() ka output dikhata hai"""
    if not combined:
        return

    final_signal = combined.get("final_signal", "WAIT")
    confidence = combined.get("confidence", 0)
    raw_score = combined.get("raw_score", 0)
    reasons = combined.get("reasons", [])

    if "STRONG BUY" in final_signal:
        sig_color = CLR_BOLD + CLR_GREEN
    elif final_signal == "BUY":
        sig_color = CLR_GREEN
    elif "STRONG SELL" in final_signal:
        sig_color = CLR_BOLD + CLR_RED
    elif final_signal == "SELL":
        sig_color = CLR_RED
    else:
        sig_color = CLR_YELLOW

    print(f"{CLR_MAGENTA}=" * 72 + CLR_RESET)
    print(f"               {CLR_BOLD}MASTER SIGNAL (TradingView + News + Market){CLR_RESET}")
    print(f"{CLR_MAGENTA}=" * 72 + CLR_RESET)
    print(f"{CLR_BOLD}Final Decision :{CLR_RESET} {sig_color}{final_signal}{CLR_RESET}   "
          f"({CLR_BOLD}Confidence:{CLR_RESET} {confidence}%  |  {CLR_BOLD}Score:{CLR_RESET} {raw_score})")
    print(f"{CLR_MAGENTA}-" * 72 + CLR_RESET)
    for r in reasons:
        print(f"   • {r}")
    print(f"{CLR_MAGENTA}=" * 72 + CLR_RESET)


# ==========================================================
# TEST ENGINE
# ==========================================================
if __name__ == "__main__":
    # ٹیسٹ ڈیٹا فار ہائی امپیکٹ نیوز
    sample_news = {
        "title": "PSX Hits Record High as Foreign Investment Inflow Accelerates",
        "source": "Dawn Business",
        "link": "https://dawn.com"
    }
    sample_result = {
        "impact_score": 9,
        "priority": "HIGH",
        "sentiment": "positive",
        "confidence": 95,
        "affected_stocks": ["OGDC", "MARI", "SYS"],
        "affected_sectors": ["Oil & Gas", "Technology"],
        "geo": ["Pakistan", "USA"],
        "reasoning_urdu": "غیر ملکی سرمایہ کاری میں اضافے کے باعث مارکیٹ میں تیزی کا رجحان دیکھا جا رہا ہے جس سے آئل اور آئی ٹی سیکٹر کو فائدہ پہنچے گا۔"
    }
    
    print("[TEST] Launching Dashboard with sample high-impact data...")
    show_dashboard(result=sample_result, news=sample_news)
