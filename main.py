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

    page = browser.new_page(
        locale="zh-TW"
    )

    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000
    )

    page.wait_for_timeout(10000)


    # 嘗試關閉 Cookie
    try:
        page.get_by_text("Đồng ý").click(timeout=3000)
    except:
        pass


    text = page.locator("body").inner_text()


    result = "目前頁面文字前500字：\n\n"
    result += text[:500]


    send(result)

    browser.close()
