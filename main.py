import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}api/sendMessage",
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


    result = "=== TPE選項定位 ===\n\n"


    try:
        page.locator("h5").filter(
            has_text="接受"
        ).click(timeout=5000)

        page.wait_for_timeout(2000)

    except:
        pass


    page.get_by_text(
        "出發地點",
        exact=True
    ).click(
        force=True,
        timeout=5000
    )

    page.wait_for_timeout(3000)


    # 找包含 TPE 的所有 div
    divs = page.locator("div").filter(
        has_text="TPE"
    )


    result += "包含TPE div數量："
    result += str(divs.count())
    result += "\n\n"


    for i in range(min(divs.count(),10)):

        try:
            txt = divs.nth(i).inner_text()

            if "桃園" in txt:

                result += "找到選項:\n"
                result += txt[:300]
                result += "\n\n"


                divs.nth(i).click(
                    force=True,
                    timeout=5000
                )

                page.wait_for_timeout(3000)

                result += "已點擊此區塊\n"

                break

        except:
            pass


    body = page.locator(
        "body"
    ).inner_text()


    if "最近到達目的地" in body:
        result += "\n選單仍存在"
    else:
        result += "\n選單已關閉"


    send(result)

    browser.close()
