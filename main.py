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


    result = "=== TPE選項分析 ===\n\n"


    # 關閉 Cookie
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


    # 搜尋相關文字

    keywords = [
        "TPE",
        "中國台北",
        "Taipei",
        "桃園"
    ]


    for k in keywords:

        elements = page.get_by_text(
            k,
            exact=False
        )

        result += f"\n關鍵字 {k} 數量：{elements.count()}\n"

        for i in range(min(elements.count(),3)):

            try:
                html = elements.nth(i).evaluate(
                    "(e)=>e.outerHTML"
                )

                result += f"\n--- {k} {i} ---\n"
                result += html[:600]
                result += "\n"

            except:
                pass


    send(result)

    browser.close()
