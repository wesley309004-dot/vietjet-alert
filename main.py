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

    result = "=== DAD定位測試 ===\n\n"


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


        page.wait_for_timeout(8000)



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
            "目的地",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(5000)



        dad_all = page.locator(
            "text=DAD"
        )


        count = dad_all.count()


        result += (
            "DAD元素數量:"
            + str(count)
            + "\n\n"
        )



        for i in range(count):

            try:

                txt = dad_all.nth(i).inner_text()

                html = dad_all.nth(i).evaluate(
                    "(e)=>e.outerHTML"
                )


                result += (
                    "第"
                    + str(i)
                    + "\n"
                    + txt
                    + "\n"
                    + html[:300]
                    + "\n\n"
                )


            except Exception as e:

                result += str(e)



        send(result)


        browser.close()



except Exception as e:


    send(
        "錯誤:\n"
        + str(e)
    )
