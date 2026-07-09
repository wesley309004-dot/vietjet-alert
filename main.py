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


    result = "=== 出發地選擇測試 ===\n\n"


    # 關 Cookie
    try:
        page.locator("h5").filter(
            has_text="接受"
        ).click(timeout=5000)

        page.wait_for_timeout(2000)

    except:
        pass


    # 點出發地

    page.get_by_text(
        "出發地點",
        exact=True
    ).click(
        force=True,
        timeout=5000
    )

    page.wait_for_timeout(3000)


    # 找臺北

    taipei = page.get_by_text(
        "臺北",
        exact=False
    )


    result += "臺北選項數量："
    result += str(taipei.count())
    result += "\n\n"


    if taipei.count() > 0:

        taipei.first.click(
            force=True
        )

        page.wait_for_timeout(3000)

        result += "成功選擇臺北\n\n"

    else:

        result += "找不到臺北\n\n"



    result += "=== 畫面文字 ===\n"

    result += page.locator(
        "body"
    ).inner_text()[:1000]


    send(result)


    browser.close()
