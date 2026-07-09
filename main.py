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

    result = "=== TPE真正選取測試 ===\n\n"


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
        )


        result += (
            "TPE數量:"
            + str(tpe.count())
            + "\n\n"
        )


        if tpe.count() > 0:


            target = tpe.first


            # 往上找真正選項盒

            for i in range(1,5):

                parent = target.locator(
                    f"xpath={'../'*i}"
                )


                txt = parent.inner_text()


                result += (
                    f"第{i}層父元素:\n"
                    + txt[:200]
                    + "\n\n"
                )


            option = target.locator(
                "xpath=../../.."
            )


            result += (
                "最後點擊元素:\n"
                + option.evaluate(
                    "(e)=>e.outerHTML"
                )[:500]
                + "\n\n"
            )


            option.dispatch_event(
                "click"
            )


            page.wait_for_timeout(5000)


            result += "已發送click事件\n"



        else:

            result += "找不到TPE\n"



        # 檢查選單

        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).count()


        result += (
            "\n目前TPE數量:"
            + str(remain)
        )


        if remain == 0:

            result += "\n選取成功"

        else:

            result += "\n選單仍存在"



        send(result)


        browser.close()



except Exception as e:

    send(
        "錯誤:\n"
        + str(e)
    )
