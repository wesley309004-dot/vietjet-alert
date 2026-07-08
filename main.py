import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )

        title = page.title()

        send_message(
            "✈️ Vietjet瀏覽器測試成功\n"
            f"頁面：{title}"
        )

        browser.close()

except Exception as e:
    send_message(
        "❌ Vietjet測試失敗\n"
        + str(e)
    )
