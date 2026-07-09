import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(text):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


try:

    result = "=== TPE選取測試 ===\n\n"


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        print("開啟網站")


        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        page.wait_for_timeout(8000)



        # Cookie

        try:

            page.locator("h5").filter(
                has_text="接受"
            ).click(
                timeout=5000
            )

            page.wait_for_timeout(2000)

        except:

            pass



        print("點擊出發地")


        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(3000)



        # 找 TPE

        tpe = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        )


        count = tpe.count()


        result += (
            "TPE數量:"
            + str(count)
            + "\n\n"
        )


        if count > 0:


            # 找包含桃園國際機場的父層

            option = tpe.first.locator(
                "xpath=../.."
            )


            result += (
                "找到選項:\n"
                + option.inner_text()
                + "\n\n"
            )


            option.click(
                force=True,
                timeout=5000
            )


            page.wait_for_timeout(3000)


            result += "已點擊TPE\n"


        else:

            result += "找不到TPE\n"



        body = page.locator(
            "body"
        ).inner_text()



        if "出發地點" in body:

            result += "\n選單仍存在"

        else:

            result += "\n選單已關閉"



        print(result)

        send(result)


        browser.close()



except Exception as e:


    send(
        "錯誤:\n"
        + str(e)
    )
