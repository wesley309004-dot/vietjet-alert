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


    result = "=== Cookie分析 ===\n\n"


    # 找所有包含接受的元素
    accept = page.get_by_text("接受", exact=False)

    result += "接受文字數量：" + str(accept.count()) + "\n\n"


    for i in range(accept.count()):
        try:
            result += (
                f"接受{i}: "
                + accept.nth(i).evaluate("(e)=>e.outerHTML")
                [:500]
                + "\n\n"
            )
        except:
            pass


    # 找 Dialog
    dialogs = page.locator('[role="dialog"]')

    result += "\nDialog數量：" + str(dialogs.count()) + "\n"

    for i in range(dialogs.count()):
        try:
            result += "\nDialog內容:\n"
            result += dialogs.nth(i).inner_text()[:500]
        except:
            pass


    send(result)

    browser.close()
