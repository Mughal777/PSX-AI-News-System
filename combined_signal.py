"""
=========================================================
PSX AI NEWS ALERT SYSTEM
combined_signal.py - MASTER SIGNAL ENGINE
=========================================================
Yeh module teen alag sources ko mila kar aik final
"STRONG BUY / BUY / WAIT / SELL / STRONG SELL" signal
banata hai:

  1) TRADINGVIEW  -> SMC PRO PLUS v3 indicator ka signal
                      (webhook_server.py ke zariye receive hota
                      hai aur signal_manager.py mein save hota hai)
  2) NEWS          -> analyzer.py ka sentiment + impact score
  3) MARKET BIAS   -> market_monitor.py ka KSE100/KMI30/Oil/USD
                      overall bias

Weights neeche WEIGHT_* variables mein hain — Irfan chahe to
inko apni marzi se badal sakta hai (total 100 rakhna behtar hai).
=========================================================
"""

from signal_manager import load_signal
from market_monitor import get_market_data, market_bias

# ---------------------------------------------------------
# WAZAN (WEIGHTS) - TradingView ko sab se zyada wazan diya
# gaya hai kyunke woh already MTF + SMC + confidence engine
# ka result hai. News aur overall market bias isay confirm
# ya reject karne ke liye use hote hain.
# ---------------------------------------------------------
WEIGHT_TRADINGVIEW = 55
WEIGHT_NEWS = 30
WEIGHT_MARKET_BIAS = 15


def _tv_component(tv_signal):
    """TradingView se aane wale JSON signal ko -1..+1 range mein convert karta hai"""
    if not tv_signal:
        return 0.0, "TradingView: کوئی سگنل موصول نہیں ہوا (webhook_server.py چلا رہے ہیں؟)"

    sig = str(tv_signal.get("signal", "")).upper()
    symbol = tv_signal.get("symbol", "N/A")
    raw_score = tv_signal.get("score", 50)
    try:
        raw_score = float(raw_score)
    except (TypeError, ValueError):
        raw_score = 50.0

    if "BUY" in sig:
        direction = 1
    elif "SELL" in sig:
        direction = -1
    else:
        direction = 0

    # score (0-100) ko strength multiplier (0..1) mein badlein
    strength = min(1.0, max(0.0, (raw_score - 50) / 50)) if direction != 0 else 0.0
    reason = f"TradingView ({symbol}): {sig} — Confidence {raw_score:.0f}%"
    return direction * strength, reason


def _news_component(news_analysis):
    """News analyzer.py ke result ko -1..+1 range mein convert karta hai"""
    if not news_analysis or not news_analysis.get("is_market_relevant", False):
        return 0.0, "News: کوئی تازہ مارکیٹ سے متعلقہ خبر نہیں"

    sentiment = str(news_analysis.get("sentiment", "neutral")).lower()
    impact = news_analysis.get("impact_score", 0)

    if sentiment == "positive":
        direction = 1
    elif sentiment == "negative":
        direction = -1
    else:
        direction = 0

    strength = min(1.0, impact / 10)
    reason = f"News: {sentiment.upper()} — Impact {impact}/10"
    return direction * strength, reason


def _bias_component(bias_text):
    """Overall market bias (KSE100/KMI30/Oil/USD) ko -1..+1 range mein convert karta hai"""
    mapping = {
        "STRONG BULLISH": 1.0,
        "BULLISH": 0.5,
        "NEUTRAL": 0.0,
        "BEARISH": -0.5,
        "STRONG BEARISH": -1.0,
    }
    val = mapping.get(bias_text, 0.0)
    reason = f"Market Bias: {bias_text}"
    return val, reason


def get_combined_signal(news_analysis=None):
    """
    TradingView + News + Market Bias ko mila kar final master
    signal deta hai. Yeh function har cycle mein call ho sakta
    hai (news wale event par, ya sirf dashboard refresh par).

    Returns:
        dict: {
            "final_signal": "STRONG BUY" | "BUY" | "WAIT" | "SELL" | "STRONG SELL",
            "confidence": int (0-100),
            "raw_score": float,
            "tv_signal": dict or None,
            "market_bias": str,
            "reasons": [str, str, str]
        }
    """
    tv_signal = load_signal()

    try:
        market_data = get_market_data()
        bias = market_bias(market_data) if market_data else "NEUTRAL"
    except Exception:
        bias = "NEUTRAL"

    tv_val, tv_reason = _tv_component(tv_signal)
    news_val, news_reason = _news_component(news_analysis)
    bias_val, bias_reason = _bias_component(bias)

    raw_score = (
        (tv_val * WEIGHT_TRADINGVIEW)
        + (news_val * WEIGHT_NEWS)
        + (bias_val * WEIGHT_MARKET_BIAS)
    )

    confidence = int(min(100, round(abs(raw_score))))

    if raw_score >= 40:
        final_signal = "STRONG BUY"
    elif raw_score >= 15:
        final_signal = "BUY"
    elif raw_score <= -40:
        final_signal = "STRONG SELL"
    elif raw_score <= -15:
        final_signal = "SELL"
    else:
        final_signal = "WAIT"

    return {
        "final_signal": final_signal,
        "confidence": confidence,
        "raw_score": round(raw_score, 1),
        "tv_signal": tv_signal,
        "market_bias": bias,
        "reasons": [tv_reason, news_reason, bias_reason],
    }


# ==========================================================
# TEST
# ==========================================================
if __name__ == "__main__":
    sample_news = {
        "is_market_relevant": True,
        "sentiment": "positive",
        "impact_score": 7,
    }
    combined = get_combined_signal(news_analysis=sample_news)
    print("=" * 60)
    print("COMBINED MASTER SIGNAL (TEST)")
    print("=" * 60)
    for k, v in combined.items():
        print(f"{k:15}: {v}")
    print("=" * 60)
