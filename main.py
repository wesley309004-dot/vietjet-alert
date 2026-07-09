import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(text):

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=20
    )

    print(r.text)



try:

    result = "=== TPE父層定位測試 ===\n\n"


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



        try:

            page.locator("h5").filter(
                has_text="接受"
            ).click(
                timeout=5000
            )

            page.wait_for_timeout(2000)

        except:

            pass



        print("開啟出發地")


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



        result += "找到TPE\n\n"



        # 第一層

        p1 = tpe.locator(
            "xpath=.."
        )

        result += (
            "第1層:\n"
            + p1.inner_text()
            + "\n\n"
        )



        # 第二層

        p2 = tpe.locator(
            "xpath=../.."
        )

        result += (
            "第2層:\n"
            + p2.inner_text()
            + "\n\n"
        )



        # 第三層

        p3 = tpe.locator(
            "xpath=../../.."
        )

        result += (
            "第3層:\n"
            + p3.inner_text()
            + "\n\n"
        )



        result += (
            "第三層HTML:\n"
            + p3.evaluate(
                "(e)=>e.outerHTML"
            )[:500]
            + "\n\n"
        )



        # 嘗試點第三層

        p3.dispatch_event(
            "click"
        )


        page.wait_for_timeout(3000)


        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).count()



        result += (
            "點擊後TPE數量:"
            + str(remain)
            + "\n"
        )


        if remain == 0:

            result += "成功關閉選單"

        else:

            result += "選單仍存在"



        send(result)


        browser.close()



except Exception as e:


    send(
        "錯誤:\n"
        + str(e)
    )
