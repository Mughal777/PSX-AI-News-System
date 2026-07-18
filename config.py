"""
config.py
=========================================================
PSX AI NEWS ALERT SYSTEM V2.1
Configuration File
=========================================================
"""

# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

APP_NAME = "PSX AI News Alert System"

APP_VERSION = "2.1"  # آپ کی پچھلی فائلوں کے مطابق ورژن اپ گریڈ کر دیا ہے

# ==========================================================
# CHECK SETTINGS
# ==========================================================

# News check interval (seconds)
CHECK_INTERVAL_SECONDS = 300      # 5 Minutes

# Minimum impact score (0-10)
MIN_IMPACT_TO_ALERT = 5

# Maximum news from each RSS feed
MAX_NEWS_PER_FEED = 10

# ==========================================================
# FILES
# ==========================================================

SEEN_NEWS_FILE = "seen_news.json"

IMAGE_CACHE_FOLDER = "cache/images"

APP_ICON = "assets/logo.ico"

ALERT_SOUND = "assets/alert.wav"

# ==========================================================
# DESKTOP NOTIFICATION (Local System Only)
# ==========================================================

ENABLE_DESKTOP_NOTIFICATION = True

NOTIFICATION_TIMEOUT = 15

ENABLE_SOUND = True

SHOW_IMAGE_NOTIFICATION = True

# ==========================================================
# NEWS SOURCES
# ==========================================================

NEWS_FEEDS = {
    "Reuters World": "https://feeds.reuters.com/Reuters/worldNews",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Business Recorder": "https://www.brecorder.com/feeds/business-recorder-pakistan",
    "Dawn Business": "https://www.dawn.com/feeds/business",
    "Profit Pakistan Today": "https://profit.pakistantoday.com.pk/feed/",
}

# ==========================================================
# WATCHLIST (Used by Portfolio Intelligence Engine)
# ==========================================================

MY_WATCHLIST = {
    "OGDC": {"name": "Oil and Gas Development", "sector": "Oil & Gas"},
    "PPL": {"name": "Pakistan Petroleum", "sector": "Oil & Gas"},
    "PSO": {"name": "Pakistan State Oil", "sector": "Oil & Gas"},
    "MARI": {"name": "Mari Petroleum", "sector": "Oil & Gas"},
    "HBL": {"name": "Habib Bank", "sector": "Banking"},
    "MCB": {"name": "MCB Bank", "sector": "Banking"},
    "UBL": {"name": "United Bank", "sector": "Banking"},
    "ENGRO": {"name": "Engro", "sector": "Fertilizer"},
    "EFERT": {"name": "Engro Fertilizer", "sector": "Fertilizer"},
    "FFC": {"name": "Fauji Fertilizer", "sector": "Fertilizer"},
    "LUCK": {"name": "Lucky Cement", "sector": "Cement"},
    "DGKC": {"name": "DG Khan Cement", "sector": "Cement"},
    "MLCF": {"name": "Maple Leaf Cement", "sector": "Cement"},
    "HUBC": {"name": "Hub Power", "sector": "Power"},
    "KEL": {"name": "K-Electric", "sector": "Power"},
    "SYS": {"name": "Systems Limited", "sector": "Technology"}
}

# ==========================================================
# IMPACT THRESHOLDS
# ==========================================================

HIGH_IMPACT_THRESHOLD = 8

MEDIUM_IMPACT_THRESHOLD = 5

LOW_IMPACT_THRESHOLD = 3
