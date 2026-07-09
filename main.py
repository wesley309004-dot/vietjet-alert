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

    result = "=== TPE React事件測試 ===\n\n"


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



        tpe = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).first



        option = tpe.locator(
            "xpath=ancestor::div[contains(@class,'MuiBox-root')][1]"
        )


        result += (
            "找到:\n"
            + option.evaluate(
                "(e)=>e.outerHTML"
            )[:500]
            + "\n\n"
        )



        # 方法1：點桃園國際機場文字

        airport = option.get_by_text(
            "桃園國際機場",
            exact=True
        )


        if airport.count() > 0:

            result += "點擊桃園文字\n"

            airport.click(
                force=True
            )

        else:

            result += "找不到桃園文字，點整區\n"

            option.click(
                force=True
            )



        page.wait_for_timeout(3000)



        # 如果沒成功，補事件

        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).count()


        if remain > 0:


            result += "第一次無效，補dispatch事件\n"


            option.dispatch_event(
                "mousedown"
            )

            option.dispatch_event(
                "mouseup"
            )

            option.dispatch_event(
                "click"
            )


            page.wait_for_timeout(3000)



        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).count()



        result += (
            "剩餘TPE:"
            + str(remain)
            + "\n"
        )



        if remain == 0:

            result += "成功選取"

        else:

            result += "仍未選取"



        send(result)


        browser.close()



except Exception as e:

    send(
        "錯誤:\n"
        + str(e)
    )
