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


    result = "=== TPE真正選取測試 ===\n\n"


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


    tpe = page.get_by_text(
        "TPE",
        exact=True
    )


    result += "TPE數量：" + str(tpe.count()) + "\n\n"


    if tpe.count() > 0:

        # 往上找祖先層級
        for level in range(1, 7):

            try:

                parent = tpe.locator(
                    "xpath=" + "/.." * level
                )

                text = parent.inner_text()

                result += (
                    f"第{level}層: "
                    + text[:100]
                    + "\n"
                )

            except:
                pass


        # 嘗試點最大容器
        try:

            parent = tpe.locator(
                "xpath=" + "/.." * 5
            )

            parent.click(
                force=True,
                timeout=5000
            )

            page.wait_for_timeout(3000)

            result += "\n已點擊第五層父元素\n"

        except Exception as e:

            result += "\n點擊失敗:\n"
            result += str(e)


    body = page.locator(
        "body"
    ).inner_text()


    if "最近到達目的地" in body:
        result += "\n選單仍存在"
    else:
        result += "\n選單消失"


    send(result)

    browser.close()
