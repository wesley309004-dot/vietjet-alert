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
        },
        timeout=20
    )



try:

    result = "=== 台灣展開後檢查 ===\n\n"


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        page.wait_for_timeout(10000)



        try:

            page.locator("h5").filter(
                has_text="接受"
            ).click(
                timeout=5000
            )

            page.wait_for_timeout(2000)

        except:

            pass



        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True
        )


        page.wait_for_timeout(5000)



        taiwan = page.get_by_text(
            "台灣 (6)",
            exact=True
        )


        taiwan.click(
            force=True
        )


        page.wait_for_timeout(8000)



        boxes = page.locator(
            "div.MuiBox-root"
        )


        result += (
            "Box數量:"
            + str(boxes.count())
            + "\n\n"
        )



        for i in range(boxes.count()):

            try:

                txt = boxes.nth(i).inner_text()

                if "桃園" in txt or "TPE" in txt or "臺北" in txt:

                    result += (
                        "找到區塊:\n"
                        + txt
                        + "\n\n"
                    )

            except:

                pass



        send(result)


        browser.close()



except Exception as e:

    send(
        "錯誤:\n"
        + str(e)
    )
