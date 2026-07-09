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

    result = "=== TPE滑鼠事件測試 ===\n\n"


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



        # 找桃園機場文字

        airport = page.locator(
            "div.jss830"
        ).filter(
            has_text="桃園國際機場"
        ).first



        result += "找到桃園文字\n"



        box = airport.bounding_box()



        if box:


            result += (
                f"座標:{box}\n"
            )


            x = box["x"] + box["width"] / 2
            y = box["y"] + box["height"] / 2


            page.mouse.move(
                x,
                y
            )


            page.mouse.down()

            page.wait_for_timeout(200)

            page.mouse.up()


            result += "完成滑鼠事件\n"



        else:

            result += "沒有座標\n"



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
