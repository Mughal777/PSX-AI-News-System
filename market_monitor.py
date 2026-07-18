"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.1
market_monitor.py
=========================================================
Live Market Monitor
"""

import yfinance as yf


# ==========================================================
# GET LAST PRICE
# ==========================================================

def get_symbol(symbol):

    try:

        ticker = yf.Ticker(symbol)

        hist = ticker.history(period="5d")

        if hist.empty:

            return None

        current = round(hist["Close"].iloc[-1], 2)

        previous = round(hist["Close"].iloc[-2], 2)

        change = round(current - previous, 2)

        percent = round((change / previous) * 100, 2)

        if change > 0:

            trend = "UP"

        elif change < 0:

            trend = "DOWN"

        else:

            trend = "FLAT"

        return {

            "price": current,

            "change": change,

            "percent": percent,

            "trend": trend

        }

    except:

        return None


# ==========================================================
# MARKET DATA
# ==========================================================

def get_market_data():

    return {

        "KSE100": get_symbol("^KSE"),

        "KMI30": get_symbol("^KMI30"),

        "OIL": get_symbol("CL=F"),

        "GOLD": get_symbol("GC=F"),

        "USD": get_symbol("PKR=X"),

    }


# ==========================================================
# MARKET BIAS
# ==========================================================

def market_bias(data):

    score = 0

    kse = data.get("KSE100")

    kmi = data.get("KMI30")

    if kse:

        if kse["change"] > 0:

            score += 2

        else:

            score -= 2

    if kmi:

        if kmi["change"] > 0:

            score += 2

        else:

            score -= 2

    oil = data.get("OIL")

    if oil:

        if oil["change"] > 0:

            score -= 1

        else:

            score += 1

    usd = data.get("USD")

    if usd:

        if usd["change"] > 0:

            score -= 1

        else:

            score += 1

    if score >= 3:

        return "STRONG BULLISH"

    elif score >= 1:

        return "BULLISH"

    elif score <= -3:

        return "STRONG BEARISH"

    elif score <= -1:

        return "BEARISH"

    else:

        return "NEUTRAL"


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    data = get_market_data()

    print()

    print("=" * 60)

    for name, info in data.items():

        print(name)

        print(info)

        print()

    print("MARKET BIAS")

    print(market_bias(data))

    print("=" * 60)