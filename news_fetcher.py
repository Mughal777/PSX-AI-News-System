"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2
news_fetcher.py
=========================================================
Professional RSS News Fetcher
"""

import hashlib
import feedparser

from config import (
    NEWS_FEEDS,
    MAX_NEWS_PER_FEED,
)

from image_fetcher import get_news_image


# ==========================================================
# Unique ID Generator
# ==========================================================

def make_news_id(link, title):

    raw = (link + title).encode("utf-8")

    return hashlib.md5(raw).hexdigest()


# ==========================================================
# Detect Video Link
# ==========================================================

def detect_video(entry):

    text = ""

    if "summary" in entry:

        text += entry.summary.lower()

    if "link" in entry:

        text += " " + entry.link.lower()

    video_words = [

        "youtube",
        "youtu.be",
        "video",
        ".mp4",
        "embed"

    ]

    for word in video_words:

        if word in text:

            return entry.get("link", "")

    return None


# ==========================================================
# Fetch News
# ==========================================================

def fetch_all_news():

    all_news = []

    seen = set()

    for source_name, rss_url in NEWS_FEEDS.items():

        try:

            feed = feedparser.parse(rss_url)

        except Exception as e:

            print(f"[ERROR] {source_name}")

            print(e)

            continue

        for entry in feed.entries[:MAX_NEWS_PER_FEED]:

            title = entry.get("title", "").strip()

            if not title:

                continue

            summary = entry.get(

                "summary",

                entry.get("description", "")

            ).strip()

            link = entry.get("link", "")

            news_id = make_news_id(link, title)

            if news_id in seen:

                continue

            seen.add(news_id)

            image = None

            try:

                image = get_news_image(link)

            except:

                pass

            video = detect_video(entry)

            item = {

                "id": news_id,

                "source": source_name,

                "title": title,

                "summary": summary,

                "link": link,

                "published": entry.get(

                    "published",

                    ""

                ),

                "image": image,

                "video": video,

            }

            all_news.append(item)

    # Latest News First

    all_news.sort(

        key=lambda x: x["published"],

        reverse=True

    )

    return all_news


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    news = fetch_all_news()

    print()

    print("Total News :", len(news))

    print()

    for item in news[:5]:

        print("=" * 60)

        print(item["title"])

        print()

        print(item["source"])

        print()

        print(item["published"])

        print()

        print(item["image"])

        print()

        print(item["video"])

        print("=" * 60)
