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


    result = "=== TPE選取測試 ===\n\n"


    # 關 Cookie
    try:
        page.locator("h5").filter(
            has_text="接受"
        ).click(timeout=5000)

        page.wait_for_timeout(2000)

    except:
        pass


    # 開啟出發地

    page.get_by_text(
        "出發地點",
        exact=True
    ).click(
        force=True,
        timeout=5000
    )

    page.wait_for_timeout(3000)


    # 找 TPE

    tpe = page.get_by_text(
        "TPE",
        exact=True
    )


    result += "TPE數量："
    result += str(tpe.count())
    result += "\n\n"


    if tpe.count() > 0:

        try:

            # 往上找可點擊的選項容器
            option = tpe.first.locator(
                "xpath=ancestor::*[self::div or self::li][1]"
            )

            option.click(
                force=True,
                timeout=5000
            )

            page.wait_for_timeout(3000)

            result += "已點擊TPE選項\n\n"

        except Exception as e:

            result += "點擊TPE失敗\n"
            result += str(e) + "\n\n"

    else:

        result += "找不到TPE\n\n"


    # 檢查選單是否還在

    body = page.locator(
        "body"
    ).inner_text()


    if "最近到達目的地" in body:
        result += "出發地選單仍存在\n"
    else:
        result += "出發地選單已關閉\n"


    result += "\n=== 畫面前500字 ===\n"
    result += body[:500]


    send(result)


    browser.close()
