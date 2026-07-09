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


def real_click(page, locator):

    box = locator.bounding_box()

    if box:

        x = box["x"] + box["width"] / 2
        y = box["y"] + box["height"] / 2


        page.mouse.move(
            x,
            y
        )

        page.mouse.down()

        page.wait_for_timeout(200)

        page.mouse.up()

        return True

    return False



try:

    result = "=== DAD真實點擊測試 ===\n\n"


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



        # 開目的地

        page.get_by_text(
            "目的地",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(5000)



        dad = page.locator(
            "div.jss829"
        ).filter(
            has_text="DAD"
        ).first



        result += "找到DAD\n"



        result += (
            "座標:"
            + str(dad.bounding_box())
            + "\n\n"
        )



        if real_click(
            page,
            dad
        ):

            result += "滑鼠點擊完成\n"

        else:

            result += "沒有座標\n"



        page.wait_for_timeout(3000)



        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="DAD"
        ).count()



        result += (
            "剩餘DAD:"
            + str(remain)
            + "\n"
        )



        if remain == 0:

            result += "目的地選取成功"

        else:

            result += "目的地仍開啟"



        send(result)


        browser.close()



except Exception as e:


    send(
        "錯誤:\n"
        + str(e)
    )
