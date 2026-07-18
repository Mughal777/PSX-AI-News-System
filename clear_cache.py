"""
=========================================================
PSX AI NEWS ALERT SYSTEM V2.2
clear_cache.py - AUTO CACHE CLEANER
=========================================================
"""
import os
import shutil
from config import IMAGE_CACHE_FOLDER, SEEN_NEWS_FILE

print("=" * 60)
print("          PSX AI SYSTEM - CACHE CLEANING UTILITY")
print("=" * 60)

# 1. تصاویر کا کیش فولڈر صاف کرنا
if os.path.exists(IMAGE_CACHE_FOLDER):
    try:
        # پورا فولڈر ڈیلیٹ کر کے دوبارہ نیا خالی فولڈر بناتا ہے
        shutil.rmtree(IMAGE_CACHE_FOLDER)
        os.makedirs(IMAGE_CACHE_FOLDER)
        print(f"[SUCCESS] Cleared all images from: {IMAGE_CACHE_FOLDER}")
    except Exception as e:
        print(f"[ERROR] Could not clear image cache: {e}")
else:
    os.makedirs(IMAGE_CACHE_FOLDER)
    print("[INFO] Image cache folder was already empty.")

# 2. نیوز ہسٹری ڈیٹا بیس کو صاف کرنا
if os.path.exists(SEEN_NEWS_FILE):
    try:
        os.remove(SEEN_NEWS_FILE)
        print(f"[SUCCESS] Deleted news history file: {SEEN_NEWS_FILE}")
        print("[INFO] This will allow old news to alert again if fresh scanning runs.")
    except Exception as e:
        print(f"[ERROR] Could not delete news file: {e}")
else:
    print("[INFO] seen_news.json was already deleted.")

print("=" * 60)
print("System cache is perfectly clean now! You can run main.py safely.")
print("=" * 60)
