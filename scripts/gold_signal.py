#!/usr/bin/env python3
import os, sys, datetime, requests

# Retrieve environment variables
GOLD_API_KEY = os.getenv("GOLD_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Validate presence
if not all([GOLD_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    print("Missing required environment variables: GOLD_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID", file=sys.stderr)
    sys.exit(1)

# Fetch gold price from API-Ninjas
try:
    resp = requests.get(
        "https://api.api-ninjas.com/v1/goldprice",
        headers={"X-Api-Key": GOLD_API_KEY},
        timeout=30,
    )
    resp.raise_for_status()
    price = resp.json()["price"]
except Exception as e:
    print(f"Failed to fetch gold price: {e}", file=sys.stderr)
    sys.exit(1)

# Build timestamp
now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# Construct Persian message
msg = f"""
جفت ارز:
نوع معامله: Buy
ورود: {price:.2f} USD
حد ضرر: {price * 0.995:.2f} USD
هدف اول: {price * 1.01:.2f} USD
هدف دوم: {price * 1.02:.2f} USD
درصد اطمینان: High
زمان: {now_utc}
"""

# Telegram API endpoint
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Payload
payload = {
    "chat_id": TELEGRAM_CHAT_ID,
    "text": msg.strip(),
    "parse_mode": "HTML",
}

# Send message
try:
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    print("Telegram message sent successfully")
except Exception as e:
    print(f"Failed to send Telegram message: {e}", file=sys.stderr)
    sys.exit(1)