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

    page.wait_for_timeout(8000)


    result = "=== Vietjet 測試 ===\n\n"


    # 關閉 Cookie
    try:
        page.locator("h5").filter(
            has_text="接受"
        ).click(
            timeout=5000
        )

        page.wait_for_timeout(3000)

        result += "Cookie關閉成功\n\n"

    except Exception as e:

        result += "Cookie關閉失敗\n"
        result += str(e) + "\n\n"


    # 確認 Cookie 是否消失
    body = page.locator("body").inner_text()

    if "我们使用 cookie" in body:
        result += "Cookie視窗仍存在\n\n"
    else:
        result += "Cookie視窗已消失\n\n"



    # 嘗試點擊出發地

    try:

        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )

        page.wait_for_timeout(3000)

        result += "出發地點點擊成功\n\n"


    except Exception as e:

        result += "出發地點點擊失敗\n"
        result += str(e) + "\n\n"



    result += "=== 點擊後文字 ===\n"

    result += page.locator(
        "body"
    ).inner_text()[:1200]


    send(result)

    browser.close()
