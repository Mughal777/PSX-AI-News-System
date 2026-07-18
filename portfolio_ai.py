"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.2
portfolio_ai.py - ADVANCED COMBINED INTELLIGENCE
=========================================================
"""

import yfinance as yf
from config import MY_WATCHLIST

MY_PORTFOLIO = {
    "MTL": {"shares": 400, "avg_price": 255.00},
    "CNERGY": {"shares": 2000, "avg_price": 10.05},
    "DCL": {"shares": 1900, "avg_price": 12.13},
    "MARI": {"shares": 115, "avg_price": 725.00}
}

def get_live_stock_price(ticker):
    """بیک اپ لاجک کے ساتھ لائیو پرائس فیچ کرتا ہے"""
    symbol_mapping = {
        "MTL": "MTL.KA", "CNERGY": "CNERGY.KA", 
        "DCL": "DCL.KA", "MARI": "MARI.KA"
    }
    yf_symbol = symbol_mapping.get(ticker, f"{ticker}.KA")
    try:
        stock = yf.Ticker(yf_symbol)
        hist = stock.history(period="5d") # 1d کے بجائے 5d ڈیٹا تاکہ مارکیٹ کلوزنگ ڈیٹا لازمی ملے
        if not hist.empty:
            return round(hist["Close"].iloc[-1], 2)
    except:
        pass
    return None

def get_technical_indicator(ticker):
    """سادہ قیمت کی بنیاد پر کسٹم مومینٹم انڈیکیٹر رینج بتاتا ہے"""
    symbol_mapping = {"MTL": "MTL.KA", "CNERGY": "CNERGY.KA", "DCL": "DCL.KA", "MARI": "MARI.KA"}
    yf_symbol = symbol_mapping.get(ticker, f"{ticker}.KA")
    try:
        stock = yf.Ticker(yf_symbol)
        hist = stock.history(period="5d")
        if len(hist) >= 2:
            prev_close = hist["Close"].iloc[-2]
            curr_close = hist["Close"].iloc[-1]
            return "BULLISH_MOMENTUM" if curr_close > prev_close else "BEARISH_MOMENTUM"
    except:
        pass
    return "NEUTRAL_TREND"

def stock_signal(ticker, analysis, market_bias_status="NEUTRAL"):
    """انڈیکیٹر بیس + نیوز امپیکٹ + سینٹیمنٹ کا کمبو فیصلہ"""
    score = 0
    
    # 1. تکنیکی انڈیکیٹر چیک کریں
    tech = get_technical_indicator(ticker)
    if tech == "BULLISH_MOMENTUM": score += 2
    elif tech == "BEARISH_MOMENTUM": score -= 2

    # 2. مارکیٹ اوور آل ٹرینڈ چیک کریں
    if market_bias_status == "BULLISH": score += 1
    elif market_bias_status == "BEARISH": score -= 1

    # 3. نیوز اور سینٹیمنٹ ڈیٹا فیوز کریں
    is_affected = ticker in analysis.get("affected_stocks", [])
    if is_affected:
        sentiment = analysis.get("sentiment", "neutral").lower()
        impact = analysis.get("impact_score", 0)
        
        if sentiment == "positive": score += (2 + (impact // 2))
        elif sentiment == "negative": score -= (2 + (impact // 2))

    # 4. کمبو ڈیسیژن لاجک (Combo Decision)
    if score >= 4: signal = "STR_BUY"
    elif score >= 2: signal = "BUY"
    elif score >= 0: signal = "HOLD"
    elif score >= -2: signal = "WAIT/WATCH"
    else: signal = "SELL"

    return {"signal": signal, "is_owned": ticker in MY_PORTFOLIO}

def calculate_portfolio_status(analysis=None, current_bias="NEUTRAL"):
    """پورٹ فولیو سمری مع فائنل لائیو رائے"""
    if analysis is None:
        analysis = {"affected_stocks": [], "sentiment": "neutral", "impact_score": 0}
        
    summary = {}
    for ticker, holding in MY_PORTFOLIO.items():
        current_price = get_live_stock_price(ticker)
        if current_price is None or current_price == 0:
            current_price = holding["avg_price"] # لائیو ڈیٹا نہ ملنے کی صورت میں پرانی پرائس فکسڈ
            
        cost_basis = holding["shares"] * holding["avg_price"]
        current_value = holding["shares"] * current_price
        pnl = current_value - cost_basis
        pnl_percent = (pnl / cost_basis) * 100 if cost_basis > 0 else 0
        
        # اسی وقت اس شیئر پر لائیو کمبو ایڈوائس نکالیں
        advice = stock_signal(ticker, analysis, current_bias)
        
        summary[ticker] = {
            "shares": holding["shares"], "avg_price": holding["avg_price"],
            "current_price": current_price, "pnl": round(pnl, 2),
            "pnl_percent": round(pnl_percent, 2), "value": round(current_value, 2),
            "ai_advice": advice["signal"]
        }
    return summary

def analyze_watchlist(analysis, market_bias_status="NEUTRAL"):
    result = {}
    for ticker in MY_WATCHLIST.keys():
        result[ticker] = stock_signal(ticker, analysis, market_bias_status)
    for ticker in MY_PORTFOLIO.keys():
        if ticker not in result:
            result[ticker] = stock_signal(ticker, analysis, market_bias_status)
    return result
