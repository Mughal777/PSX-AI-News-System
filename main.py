import json, os, time, traceback
from datetime import datetime

from config import APP_NAME, APP_VERSION, CHECK_INTERVAL_SECONDS, SEEN_NEWS_FILE
from news_fetcher import fetch_all_news
from analyzer import analyze_news
from notifier import send_news_alert
from dashboard import show_dashboard, show_combined_panel, clear
from market_monitor import get_market_data, market_bias
from portfolio_ai import analyze_watchlist, calculate_portfolio_status
from combined_signal import get_combined_signal

# عالمی رن ٹائم ڈوپلی کیٹ فلٹر (ڈبل پروٹیکشن)
SEEN_TITLES = set()

def load_seen_news():
    """ہارڈ ڈرائیو سے پرانی دیکھی گئی خبروں کی لسٹ لوڈ کرتا ہے"""
    if os.path.exists(SEEN_NEWS_FILE):
        try:
            with open(SEEN_NEWS_FILE, "r", encoding="utf-8") as f: 
                return set(json.load(f))
        except: 
            return set()
    return set()

def save_seen_news(seen):
    """دیکھی گئی خبروں کے ڈیٹا بیس کو ہارڈ ڈرائیو پر محفوظ کرتا ہے"""
    try:
        with open(SEEN_NEWS_FILE, "w", encoding="utf-8") as f: 
            json.dump(list(seen)[-3000:], f, indent=4)
    except Exception as e: 
        print(f"[DB SAVE ERROR]: {e}")

def print_live_portfolio_summary(analysis=None, current_bias="NEUTRAL"):
    portfolio_data = calculate_portfolio_status(analysis, current_bias)
    if not portfolio_data: return

    print("=" * 72)
    print("                    YOUR LIVE PORTFOLIO & AI DECISION")
    print("=" * 72)
    
    total_investment = 0
    total_current_val = 0
    
    for stock, info in portfolio_data.items():
        cost = info["shares"] * info["avg_price"]
        total_investment += cost
        total_current_val += info["value"]
        
        status_icon = "🟢 +Rs." if info["pnl"] >= 0 else "🔴 -Rs."
        print(f"{stock:6} | Buy: {info['avg_price']:6.2f} | Live: {info['current_price']:6.2f} | P&L: {status_icon}{abs(info['pnl']):7.2f} | AI: \033[93m{info['ai_advice']:10}\033[0m")
        
    total_pnl = total_current_val - total_investment
    total_pnl_pct = (total_pnl / total_investment) * 100 if total_investment > 0 else 0
    
    print("-" * 72)
    print(f"NET PORTFOLIO VALUE : Rs. {total_current_val:,.2f}")
    print(f"TOTAL ACCUMULATED P&L: Rs. {total_pnl:+,.2f} ({total_pnl_pct:.2f}%)")
    print("=" * 72)

def process_news(news, seen, current_bias):
    news_id = str(news.get("id", ""))
    news_title = news.get("title", "").strip().lower()

    # فلٹر 1: اگر آئی ڈی پہلے سے ڈیٹا بیس میں موجود ہے
    if news_id in seen: return
    
    # فلٹر 2: اگر ملتی جلتی سرخی اس سائیکل میں آ چکی ہے
    if news_title in SEEN_TITLES: return

    # 🛑 اسمارٹ اے آئی فلٹر
    result = analyze_news(news)
    impact = result.get("impact_score", 3)
    sentiment = result.get("sentiment", "neutral").lower()
    
    # فالتو اور نیوٹرل خبریں الرٹ/ڈیش بورڈ پر جانے سے روکیں
    if impact < 6 and sentiment == "neutral":
        print(f"[FILTERED]: Low impact neutral news skipped -> {news.get('title')[:30]}")
        return

    # فوری لاک لاجک
    seen.add(news_id)
    SEEN_TITLES.add(news_title)
    save_seen_news(seen)
    
    # ڈیش بورڈ اپ ڈیٹ کریں
    show_dashboard(result=result, news=news)

    # TradingView + News + Market Bias کو ملا کر ماسٹر سگنل دکھائیں
    combined = get_combined_signal(news_analysis=result)
    show_combined_panel(combined)

    # ونڈوز پاپ اپ نوٹیفیکیشن بھیجیں (WhatsApp ہٹا دیا گیا ہے)
    try:
        send_news_alert(news, result)
    except Exception as ne:
        print(f"[ALERT POPUP ERROR]: {ne}")
    
    time.sleep(2) 
    clear()
    print_live_portfolio_summary(analysis=result, current_bias=current_bias)
    show_combined_panel(combined)

def run_once(seen):
    """پورٹ فولیو لائیو اپڈیٹ اور نیوز سکیننگ کا ایک مکمل سائیکل چلاتا ہے"""
    SEEN_TITLES.clear()
    
    market_data = get_market_data()
    bias = market_bias(market_data) if market_data else "NEUTRAL"
    
    clear()
    print("=" * 72)
    print(f"           {APP_NAME} v{APP_VERSION} - ACTIVE LIVE MONITOR")
    print("=" * 72)
    print(f"Date/Time  : {datetime.now().strftime('%d-%b-%Y %I:%M:%S %p')}")
    print(f"Market Bias: {bias}")
    print(f"Database   : {len(seen)} News Logged")
    print(f"Status     : Live Scanning PSX News Feed...")

    # کوئی تازہ خبر نہ ہو تب بھی TradingView سگنل + مارکیٹ بائیس والا ماسٹر پینل دکھائیں
    combined = get_combined_signal(news_analysis=None)
    show_combined_panel(combined)

    print_live_portfolio_summary(analysis=None, current_bias=bias)

    news_list = fetch_all_news()
    for news in news_list:
        try:
            process_news(news, seen, bias)
        except Exception as e:
            pass

def main():
    seen = load_seen_news()
    
    # 🌟 سمارٹ چیک: اگر یہ گٹ ہب ایکشنز پر چل رہا ہے
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print("[GITHUB MODE]: Running scan once and exiting...")
        run_once(seen)
        print("[GITHUB MODE]: Scan completed. Exiting safely.")
        return 

    # 💻 لوکل کمپیوٹر موڈ
    print("[LOCAL MODE]: Running infinite loop on your PC...")
    
    while True:
        try:
            run_once(seen)
            # ہر 30 سیکنڈ بعد لائیو مارکیٹ/پورٹ فولیو ریفریش کرے گا
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n[INFO] Engine Stopped By User.")
            break
        except Exception as e:
            print(f"\n💥 [ENGINE ERROR]: {e}")
            print(traceback.format_exc())
            print("[INFO] Retrying in 10 seconds...\n")
            time.sleep(10)

if __name__ == "__main__": 
    main()
