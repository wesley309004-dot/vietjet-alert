import os
import requests

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

url = "https://www.vietjetair.com/en/pages/promotions"

keywords = [
    "Japan",
    "Sale",
    "Promotion",
    "Flash Sale",
    "Discount"
]

try:
    r = requests.get(url, timeout=20)
    text = r.text.lower()

    found = []

    for k in keywords:
        if k.lower() in text:
            found.append(k)

    if found:
        message = (
            "✈️ Vietjet 促銷偵測！\n\n"
            "發現關鍵字：\n"
            + ", ".join(found)
            + "\n\n請立即查看官網"
        )

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": message
            }
        )

except Exception as e:
    print(e)
