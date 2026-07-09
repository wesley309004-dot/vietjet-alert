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

    page = browser.new_page(locale="zh-TW")

    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000
    )

    page.wait_for_timeout(8000)


    # Cookie
    try:
    page.locator("button").filter(has_text="接受").click(timeout=5000)
    page.wait_for_timeout(3000)
except Exception as e:
    print(e)


    result = "=== 出發地測試 ===\n\n"


    try:
        # 點擊出發地文字附近區域
        page.get_by_text(
            "出發地點",
            exact=True
        ).click(timeout=5000)

        page.wait_for_timeout(3000)

        result += "成功點擊出發地點\n\n"

    except Exception as e:

        result += "點擊失敗\n"
        result += str(e)


    # 點擊後抓頁面文字
    text = page.locator("body").inner_text()

    result += "=== 後續文字 ===\n"
    result += text[:1000]


    send(result)

    browser.close()
