import os
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto(
        "https://www.vietjetair.com/zh-TW/select-flight",
        timeout=60000
    )

    page.wait_for_timeout(10000)

    buttons = page.locator("button")

    result = "按鈕數量：" + str(buttons.count()) + "\n\n"

    for i in range(buttons.count()):
        try:
            text = buttons.nth(i).inner_text()
            result += f"{i}: {text}\n"
        except:
            pass

    send(result)

    browser.close()
