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

    try:
        page.get_by_text("接受").click(timeout=3000)
        page.wait_for_timeout(3000)
    except:
        pass


    result = "=== 元件分析 ===\n\n"


    # 找 role
    combos = page.locator('[role="combobox"]')

    result += "Combobox數量：" + str(combos.count()) + "\n\n"

    for i in range(combos.count()):
        try:
            result += (
                f"{i}: "
                + combos.nth(i).inner_text()
                + "\n"
            )
        except:
            pass


    # 找包含文字的元素

    keywords = [
        "出發地點",
        "目的地",
        "出發日期",
        "返程日期",
        "乘客"
    ]

    result += "\n=== 關鍵文字 ===\n"

    for k in keywords:
        count = page.get_by_text(k, exact=False).count()
        result += f"{k}: {count}\n"


    send(result)

    browser.close()
