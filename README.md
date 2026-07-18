# PSX AI News & Signal Alert System

WhatsApp / Green API مکمل طور پر ہٹا دیا گیا ہے۔ اب یہ پروجیکٹ صرف تین چیزوں پر مشتمل ہے:

1. **TradingView** — آپ کا موجودہ SMC PRO PLUS v3 indicator (پہلے سے بنا ہوا)
2. **Python (VS Code)** — نیوز سکیننگ، سینٹیمنٹ تجزیہ، پورٹ فولیو ٹریکنگ
3. **GitHub** — کوڈ ہوسٹنگ + ہر گھنٹے خودکار سکین (GitHub Actions)

نئی چیز یہ ہے: **`combined_signal.py`** — یہ TradingView کے سگنل، تازہ خبروں کے
sentiment/impact، اور مجموعی مارکیٹ بائیس (KSE100/KMI30/Oil/USD) کو ملا کر
ایک **Master Signal** (STRONG BUY / BUY / WAIT / SELL / STRONG SELL) بناتا ہے۔

---

## سیٹ اپ کے مراحل

### 1) پیکجز انسٹال کریں
```
pip install -r requirements.txt
```

### 2) `config.py` میں اپنی watchlist چیک کریں
`MY_WATCHLIST` میں اپنے سٹاکس کے ٹکر، کمپنی کا نام، اور سیکٹر شامل ہیں — ضرورت کے مطابق ترمیم کریں۔

### 3) TradingView سے سگنل وصول کرنے کے لیے webhook server چلائیں
اگر آپ چاہتے ہیں کہ TradingView کا الرٹ سیدھا Python میں آئے، تو ایک الگ ٹرمینل میں یہ چلائیں:
```
python webhook_server.py
```
یہ `http://<your-pc-ip>:5000/webhook` پر سنے گا۔ TradingView الرٹ میں webhook URL یہی
دیں (اگر لوکل پی سی پر ٹیسٹ کرنا ہو تو [ngrok](https://ngrok.com) جیسا ٹول استعمال کریں
تاکہ عوامی URL بنے)۔ TradingView کے alert message میں کم از کم یہ فیلڈز JSON میں بھیجیں:
```json
{ "symbol": "OGDC", "signal": "BUY", "score": 82 }
```
یہ خودکار طور پر `last_signal.json` میں محفوظ ہو جائے گا، جسے main.py اور combined_signal.py پڑھتے ہیں۔

### 4) مین سسٹم چلائیں
```
python main.py
```
یہ ہر تھوڑی دیر بعد خبریں چیک کرے گا، ڈیش بورڈ اپڈیٹ کرے گا، اور **Master Signal Panel**
دکھائے گا جو TradingView + News + Market Bias کا ملا جلا فیصلہ ہے۔

---

## Master Signal کیسے بنتا ہے (`combined_signal.py`)

| Source        | Weight | تفصیل                                              |
|---------------|--------|-----------------------------------------------------|
| TradingView   | 55%    | `last_signal.json` سے (webhook کے ذریعے موصول)      |
| News          | 30%    | `analyzer.py` کا sentiment + impact score            |
| Market Bias   | 15%    | KSE100 / KMI30 / Oil / USD کا مجموعی رجحان           |

یہ weights `combined_signal.py` کے اوپر والے `WEIGHT_*` variables میں ہیں — آسانی سے تبدیل کر سکتے ہیں۔

---

## Desktop Notifications
WhatsApp کی جگہ اب صرف Windows desktop pop-up (`win11toast`) استعمال ہوتا ہے —
یہ صرف Windows پر کام کرتا ہے، GitHub Actions/Linux پر خودکار طور پر skip ہو جاتا ہے،
کوئی ایرر نہیں دیتا۔ `config.py` میں `ENABLE_DESKTOP_NOTIFICATION = False` کر کے بند بھی کر سکتے ہیں۔

## GitHub Actions (خودکار سکین)
`.github/workflows/run_bot.yml` ہر گھنٹے `main.py` کو GitHub کے سرور پر چلاتا ہے
(صرف news scan اور log — کوئی secret/token درکار نہیں، کیونکہ WhatsApp ہٹا دیا گیا ہے)۔
نوٹ: GitHub Actions پر `webhook_server.py` چلانا ممکن نہیں کیونکہ یہ ہمیشہ آن رہنے
والا سرور مانگتا ہے — وہ اپنے PC پر یا کسی چھوٹے cloud VM پر چلائیں۔

## ⚠️ سیکیورٹی نوٹ
پرانی فائلوں (`notifier.py`, `news_bot.py`) میں Green API کا instance ID اور token
براہِ راست کوڈ میں لکھے ہوئے تھے۔ یہ فائلیں اب حذف/صاف کر دی گئی ہیں، لیکن اگر یہ
پہلے کبھی GitHub پر push ہوئی تھیں تو وہ token اب بھی git history میں موجود ہو سکتا
ہے۔ **براہِ کرم Green API کنسول پر جا کر وہ token فوراً regenerate/revoke کر دیں**،
چاہے اب استعمال نہ بھی ہو رہا ہو۔
