"""
=========================================================
PSX AI NEWS ALERT SYSTEM
notifier.py - DESKTOP NOTIFICATIONS ONLY
=========================================================
WhatsApp / Green API is fully removed from this project.
Ab sirf Windows desktop pop-up alert bhejta hai (agar
win11toast library available ho aur ENABLE_DESKTOP_NOTIFICATION
config.py mein True ho). GitHub Actions / Linux / Mac par
yeh function chup chaap skip ho jata hai, error nahi deta.
=========================================================
"""
import os
import time
import requests

from config import (
    ENABLE_DESKTOP_NOTIFICATION,
    IMAGE_CACHE_FOLDER,
    APP_ICON
)
from image_fetcher import get_news_image

# win11toast sirf Windows par kaam karta hai. Cloud/Linux/Mac par
# import fail ho sakta hai — is liye safe try/except.
try:
    from win11toast import toast
    _TOAST_AVAILABLE = True
except Exception:
    _TOAST_AVAILABLE = False

if not os.path.exists(IMAGE_CACHE_FOLDER):
    os.makedirs(IMAGE_CACHE_FOLDER)


def download_news_image(image_url, news_id):
    """انٹرنیٹ سے خبر کی تصویر نوٹیفیکیشن کے لیے ڈاؤن لوڈ کرتا ہے"""
    if not image_url:
        return None
    try:
        clean_id = "".join([c for c in str(news_id) if c.isalnum()])
        local_path = os.path.join(IMAGE_CACHE_FOLDER, f"{clean_id}.png")
        if os.path.exists(local_path):
            return os.path.join(os.getcwd(), local_path)

        response = requests.get(image_url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            return os.path.join(os.getcwd(), local_path)
    except Exception:
        pass
    return None


def send_news_alert(news, result):
    """صرف ونڈوز ڈیسک ٹاپ پاپ اپ نوٹیفیکیشن بھیجتا ہے (WhatsApp ہٹا دیا گیا ہے)"""
    if not ENABLE_DESKTOP_NOTIFICATION:
        return
    if not _TOAST_AVAILABLE:
        # Linux / GitHub Actions / Mac par toast library nahi hoti — chup chaap skip
        return

    title = news.get("title", "PSX ALERT")
    source = news.get("source", "Market Source")
    impact = result.get("impact_score", 3)
    sentiment = result.get("sentiment", "neutral").upper()
    news_link = news.get("link", "")

    if impact >= 7:
        alert_title = f"🚨 BREAKING: {title[:50]}..."
    else:
        alert_title = f"🔔 PSX ALERT: {title[:50]}..."

    urdu_msg = result.get("reasoning_urdu", "")
    alert_msg = f"Source: {source} | Impact: {impact}/10 | [{sentiment}]\n\n{urdu_msg[:120]}...\n\nLink: {news_link}"

    try:
        raw_img_url = result.get("image_url") or get_news_image(news_link)
        local_image_path = download_news_image(raw_img_url, news.get("id", time.time()))

        icon_path = os.path.join(os.getcwd(), APP_ICON) if os.path.exists(APP_ICON) else None

        toast_kwargs = {
            "title": alert_title,
            "body": alert_msg,
            "icon": icon_path
        }

        if local_image_path and os.path.exists(local_image_path):
            toast_kwargs["image"] = local_image_path

        if impact >= 7:
            toast_kwargs["audio"] = "ms-winsoundevent:Notification.Looping.Alarm2"
        else:
            toast_kwargs["audio"] = "ms-winsoundevent:Notification.Default"

        if news_link:
            toast_kwargs["button"] = {"activationType": "protocol", "arguments": news_link, "content": "Read Full News"}

        toast(**toast_kwargs)
    except Exception as e:
        print(f"[NOTIFIER ERROR]: {e}")
