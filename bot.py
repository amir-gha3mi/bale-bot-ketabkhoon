import requests
import time
from datetime import datetime
import csv
import os

# توکن را از متغیر محیطی می‌خوانیم
TOKEN = os.getenv("BALE_TOKEN")
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}/"

offset = 0  # برای دریافت پیام‌های جدید

def save_to_csv(username, value):
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([username, value, datetime.now().isoformat()])

def get_updates():
    url = BASE_URL + "getUpdates"
    resp = requests.get(url, params={"offset": offset})
    return resp.json()

def send_message(chat_id, text):
    url = BASE_URL + "sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def main():
    global offset
    print("Bot started...")

    while True:
        updates = get_updates()

        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    username = msg["chat"].get("username", "no-username")
                    text = msg.get("text", "")

                    # بررسی اینکه متن عدد هست یا نه
                    if text.isdigit():
                        save_to_csv(username, text)
                        send_message(chat_id, "عدد ذخیره شد ✔️")
                    else:
                        send_message(chat_id, "یک عدد ارسال کن 😊")

        time.sleep(1)

if __name__ == "__main__":
    main()

