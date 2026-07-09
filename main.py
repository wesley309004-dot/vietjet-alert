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

    result = "=== Vietjet目的地測試 ===\n\n"


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



        # 出發地

        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(3000)



        # TPE

        airport = page.locator(
            "div.jss830"
        ).filter(
            has_text="桃園國際機場"
        ).first



        real_click(
            page,
            airport
        )


        page.wait_for_timeout(3000)



        result += "TPE完成\n"



        # 點目的地

        page.get_by_text(
            "目的地",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(3000)



        # 找 DAD

        dad = page.locator(
            "div.jss829"
        ).filter(
            has_text="DAD"
        ).first



        count = dad.count()


        result += (
            "DAD數量:"
            + str(count)
            + "\n"
        )



        if count > 0:


            parent = dad.locator(
                "xpath=ancestor::div[contains(@class,'MuiBox-root')][1]"
            )


            result += (
                "找到:\n"
                + parent.evaluate(
                    "(e)=>e.outerHTML"
                )[:300]
                + "\n"
            )



            real_click(
                page,
                dad
            )


            page.wait_for_timeout(3000)


            result += "已點擊DAD\n"



        else:

            result += "找不到DAD\n"



        # 檢查

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



        send(result)


        browser.close()



except Exception as e:


    send(
        "錯誤:\n"
        + str(e)
    )
