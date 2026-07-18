"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.2
analyzer.py - FULL INTEGRATED FILE (PART A + B)
=========================================================
"""

import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from config import MY_WATCHLIST

# ==========================================================
# INITIALIZE AI & DICTIONARIES (Part A)
# ==========================================================
vader = SentimentIntensityAnalyzer()

HIGH_IMPACT_KEYWORDS = {
    "war":10, "attack":9, "missile":9, "airstrike":9, "invasion":10, "nuclear":10,
    "terrorist":9, "terrorism":9, "bomb":9, "explosion":8, "military":8, "army":8,
    "conflict":8, "border clash":8, "martial law":10, "emergency":8, "default":10,
    "bankruptcy":8, "sanctions":8, "embargo":8, "ceasefire":6, "oil shock":9
}

MEDIUM_IMPACT_KEYWORDS = {
    "imf":7, "sbp":7, "policy rate":7, "interest rate":7, "inflation":6, "gdp":5,
    "budget":5, "tax":5, "exports":5, "imports":5, "trade":5, "loan":5,
    "credit rating":6, "moody":6, "fitch":6, "recession":7, "devaluation":7,
    "rupee":6, "usd":6, "dollar":6, "crude":6, "oil":6, "gas":5, "gold":5
}

POSITIVE_KEYWORDS = {
    "profit":4, "growth":4, "record profit":6, "investment":5, "agreement":4,
    "deal":5, "recovery":5, "upgrade":5, "stable":3, "bullish":5, "rally":5,
    "surge":5, "expansion":5, "strong earnings":6
}

NOTE_KEYWORDS = {
    "loss":5, "decline":5, "drop":5, "crash":8, "bearish":5, "selloff":7,
    "panic":8, "fear":7, "downgrade":6, "bankrupt":8, "fraud":8, "corruption":7
}

# پرانے نام کی بیک ورڈ سپورٹ کے لیے NEGATIVE_KEYWORDS کو ہینڈل کریں
NEGATIVE_KEYWORDS = NOTE_KEYWORDS

SECTOR_KEYWORDS = {
    "Oil & Gas": ["oil", "gas", "crude", "petroleum", "lng", "opec"],
    "Banking": ["bank", "interest rate", "sbp", "policy rate"],
    "Cement": ["cement", "construction", "housing"],
    "Power": ["electricity", "power", "energy", "generation"],
    "Technology": ["software", "technology", "ai", "cloud", "cyber"],
    "Fertilizer": ["fertilizer", "urea", "dap", "agriculture"]
}

BREAKING_WORDS = ["breaking", "urgent", "developing", "live", "just in"]
GEOPOLITICAL_WORDS = ["iran", "israel", "usa", "china", "india", "pakistan", "ukraine", "russia", "middle east", "gulf"]

# ==========================================================
# GOOGLE TRANSLATION ENGINE (Part B)
# ==========================================================
from deep_translator import GoogleTranslator

def translate_to_urdu(text):
    """deep-translator پیکج کو استعمال کرتے ہوئے پکا اور صاف اردو ترجمہ نکالتا ہے"""
    if not text:
        return "کوئی تفصیل دستیاب نہیں ہے۔"
    try:
        # یہ بغیر کسی بلاک یا لیمیٹیشن کے ڈائریکٹ ترجمہ کرے گا
        translated = GoogleTranslator(source='en', target='ur').translate(text)
        return translated
    except Exception as e:
        # اگر انٹرنیٹ کا کوئی عارضی مسئلہ ہو تو بیک اپ لاجک
        return f"[ترجمہ دستیاب نہیں: {text[:60]}...]"


# ==========================================================
# MATCH & SCORE ENGINES (Part B)
# ==========================================================
def find_stocks(text):
    found = []
    lower = text.lower()
    for ticker, data in MY_WATCHLIST.items():
        if ticker.lower() in lower or data["name"].lower() in lower:
            found.append(ticker)
            
    portfolio_tickers = ["MTL", "CNERGY", "DCL", "MARI"]
    for ticker in portfolio_tickers:
        if ticker.lower() in lower and ticker not in found:
            found.append(ticker)
    return sorted(list(set(found)))

def find_sectors(text):
    found = []
    lower = text.lower()
    for sector, words in SECTOR_KEYWORDS.items():
        for word in words:
            if word in lower:
                found.append(sector)
                break
    return sorted(list(set(found)))

def build_text(news_item):
    title = news_item.get("title", "")
    summary = news_item.get("summary", "") or news_item.get("description", "")
    return f"{title} {summary}".lower()

def detect_sentiment(text):
    score = vader.polarity_scores(text)
    compound = score["compound"]
    if compound >= 0.20: sentiment = "positive"
    elif compound <= -0.20: sentiment = "negative"
    else: sentiment = "neutral"

    for kw in POSITIVE_KEYWORDS:
        if kw in text: sentiment = "positive"
    for kw in NEGATIVE_KEYWORDS:
        if kw in text: sentiment = "negative"
    return sentiment, compound

def keyword_score(text):
    score = 0
    matched = []
    for word, weight in HIGH_IMPACT_KEYWORDS.items():
        if word in text:
            score += weight
            matched.append(word)
    for word, weight in MEDIUM_IMPACT_KEYWORDS.items():
        if word in text:
            score += weight
            matched.append(word)
    for word, weight in POSITIVE_KEYWORDS.items():
        if word in text:
            score += weight
            matched.append(word)
    for word, weight in NEGATIVE_KEYWORDS.items():
        if word in text:
            score += weight
            matched.append(word)
    return score, matched

def is_breaking_news(text):
    for word in BREAKING_WORDS:
        if word in text: return True
    return False

def detect_geo(text):
    countries = []
    for country in GEOPOLITICAL_WORDS:
        if country in text: countries.append(country.upper())
    return countries

def calculate_impact(keyword_points, stocks, sectors, geo, breaking):
    impact = keyword_points
    impact += len(stocks) * 2
    impact += len(sectors)
    impact += len(geo)
    if breaking: impact += 2
    if impact > 10: impact = 10
    if impact < 1: impact = 3
    return int(impact)

def confidence_score(keyword_points, stocks, sectors):
    score = 40
    score += keyword_points * 4
    score += len(stocks) * 10
    score += len(sectors) * 5
    if score > 100: score = 100
    return int(score)

def market_relevant(keyword_points, stocks, sectors, geo):
    if keyword_points > 0 or stocks or sectors or geo: return True
    return False

# ==========================================================
# MAIN ENTRY CONNECTION FUNCTION
# ==========================================================
def analyze_news(news_item):
    full_text_lower = build_text(news_item)
    
    points, matched_kws = keyword_score(full_text_lower)
    stocks = find_stocks(full_text_lower)
    sectors = find_sectors(full_text_lower)
    geo = detect_geo(full_text_lower)
    breaking = is_breaking_news(full_text_lower)
    
    sentiment, compound = detect_sentiment(full_text_lower)
    
    impact = calculate_impact(points, stocks, sectors, geo, breaking)
    confidence = confidence_score(points, stocks, sectors)
    is_relevant = market_relevant(points, stocks, sectors, geo)
    
    raw_title = news_item.get("title", "")
    raw_summary = news_item.get("summary", "") or news_item.get("description", "")
    english_payload = f"{raw_title}. {raw_summary}"
    
    urdu_translation = translate_to_urdu(english_payload)
    
    return {
        "is_market_relevant": is_relevant,
        "impact_score": impact,
        "priority": "HIGH" if impact >= 7 else ("MEDIUM" if impact >= 4 else "LOW"),
        "sentiment": sentiment,
        "confidence": confidence,
        "affected_stocks": stocks,
        "affected_sectors": sectors,
        "geo": geo,
        "reasoning_urdu": urdu_translation
    }
