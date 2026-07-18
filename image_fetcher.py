"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.2
image_fetcher.py - UPGRADED WITH TEXT SCRAPER
=========================================================
News Image & Full Article Text Extractor for AI Translation
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}

def _absolute_url(base, url):
    if not url:
        return None
    if url.startswith("http"):
        return url
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        parsed_uri = urlparse(base)
        domain = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
        return domain.rstrip("/") + url
    return url

def get_news_data(news_url):
    """
    خبر کا لنک لے کر تصویر اور تفصیلی ٹیکسٹ دونوں نکالتا ہے تاکہ AI اردو ترجمہ کر سکے
    Returns:
        dict: {"image_url": str or None, "article_text": str or None}
    """
    data = {"image_url": None, "article_text": None}
    if not news_url or not news_url.startswith("http"):
        return data

    try:
        response = requests.get(news_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return data
            
        soup = BeautifulSoup(response.text, "html.parser")

        # 1. تصویر نکالنے کا لاجک (Image Extraction)
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            data["image_url"] = og["content"]
        else:
            tw = soup.find("meta", attrs={"name": "twitter:image"})
            if tw and tw.get("content"):
                data["image_url"] = tw["content"]
            else:
                img = soup.find("img")
                if img:
                    src = img.get("src") or img.get("data-src") or img.get("data-original")
                    if src:
                        data["image_url"] = _absolute_url(news_url, src)

        # 2. خبر کا تفصیلی متن نکالنا (Article Text Extraction for Urdu Translation)
        # زیادہ تر نیوز ویب سائٹس پر خبر پیراگراف (<p>) ٹیگز میں ہوتی ہے
        paragraphs = soup.find_all("p")
        text_content = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            # فالتو لنکس، اشتہارات یا کوکیز کے چھوٹے ٹیکسٹ کو فلٹر کریں
            if len(text) > 40 and not text.startswith("Copyright") and not text.startswith("Read more"):
                text_content.append(text)
        
        # پہلے 4 یا 5 اہم پیراگراف جمع کریں تاکہ AI لوڈ زیادہ نہ ہو اور ترجمہ پرفیکٹ آئے
        if text_content:
            data["article_text"] = "\n".join(text_content[:5])

    except Exception:
        pass

    return data

# پرانے فنکشن کی بیک ورڈ سپورٹ تاکہ باقی کوڈ کریش نہ ہو
def get_news_image(news_url):
    res = get_news_data(news_url)
    return res["image_url"]
