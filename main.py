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

    result = "=== TPE點擊V3 ===\n\n"


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
        ).first



        result += "找到TPE\n"



        # 找城市名稱臺北

        city = tpe.locator(
            "xpath=../div[contains(@class,'jss828')]"
        )


        result += (
            "城市文字:"
            + city.inner_text()
            + "\n"
        )



        # 點城市

        city.click(
            force=True
        )


        page.wait_for_timeout(3000)



        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).count()



        result += (
            "第一次後TPE:"
            + str(remain)
            + "\n"
        )



        if remain > 0:


            # 重新抓，避免 stale

            tpe2 = page.locator(
                "div.jss829"
            ).filter(
                has_text="TPE"
            ).first


            tpe2.press(
                "Enter"
            )


            page.wait_for_timeout(3000)



        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).count()



        result += (
            "最後TPE:"
            + str(remain)
            + "\n"
        )


        if remain == 0:

            result += "成功"

        else:

            result += "失敗"



        send(result)


        browser.close()



except Exception as e:

    send(
        "錯誤:\n"
        + str(e)
    )
