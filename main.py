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

    result = "=== DAD等待測試 ===\n\n"


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

            page.wait_for_timeout(3000)

        except:

            pass



        page.get_by_text(
            "目的地",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        result += "已開目的地\n"


        page.wait_for_timeout(8000)



        body = page.locator(
            "body"
        ).inner_text()



        if "DAD" in body:

            result += "body找到DAD\n"

        else:

            result += "body沒有DAD\n"



        codes = page.locator(
            "div.jss829"
        )


        count = codes.count()


        result += (
            "jss829數量:"
            + str(count)
            + "\n\n"
        )



        for i in range(min(count,50)):

            try:

                txt = codes.nth(i).inner_text()

                if txt.strip():

                    result += txt + "\n"

            except:

                pass



        send(result)


        browser.close()



except Exception as e:


    send(
        "錯誤:\n"
        + str(e)
    )
