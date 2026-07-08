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

    inputs = page.locator("input")

    result = "訂票頁輸入框數量：" + str(inputs.count()) + "\n\n"

    for i in range(inputs.count()):
        placeholder = inputs.nth(i).get_attribute("placeholder")
        name = inputs.nth(i).get_attribute("name")
        result += f"{i}: placeholder={placeholder}, name={name}\n"

    send(result)

    browser.close()
