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


    # Cookie
    try:
        page.get_by_text("接受").click(timeout=3000)
        page.wait_for_timeout(3000)
    except:
        pass


    result = "=== 泰越捷頁面測試 ===\n\n"


    # 找文字中的貨幣
    body = page.locator("body").inner_text()

    if "USD" in body:
        result += "目前偵測到貨幣：USD\n"

    if "TWD" in body:
        result += "目前偵測到貨幣：TWD\n"


    # 列出 input
    inputs = page.locator("input")

    result += "\n輸入框數量：" + str(inputs.count()) + "\n\n"


    for i in range(inputs.count()):
        try:
            result += (
                f"{i}: "
                f"placeholder={inputs.nth(i).get_attribute('placeholder')} "
                f"name={inputs.nth(i).get_attribute('name')}\n"
            )
        except:
            pass


    # 列出按鈕
    buttons = page.locator("button")

    result += "\n按鈕數量：" + str(buttons.count()) + "\n\n"


    for i in range(min(buttons.count(),20)):
        try:
            txt = buttons.nth(i).inner_text()
            if txt.strip():
                result += f"{i}: {txt}\n"
        except:
            pass


    send(result)

    browser.close()
