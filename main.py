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

    if not box:
        return False

    x = box["x"] + box["width"]/2
    y = box["y"] + box["height"]/2

    page.mouse.move(x,y)
    page.mouse.down()
    page.wait_for_timeout(200)
    page.mouse.up()

    return True



try:

    result = "=== TPE後目的地DOM ===\n\n"


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



        # 出發地

        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True
        )


        page.wait_for_timeout(5000)



        page.get_by_text(
            "台灣 (6)",
            exact=True
        ).click(
            force=True
        )


        page.wait_for_timeout(5000)



        tpe = page.locator(
            "div.MuiBox-root"
        ).filter(
            has_text="TPE"
        ).filter(
            has_text="桃園國際機場"
        ).first


        real_click(
            page,
            tpe
        )


        result += "TPE完成\n"


        page.wait_for_timeout(5000)



        # 開目的地

        page.get_by_text(
            "目的地",
            exact=True
        ).click(
            force=True
        )


        result += "目的地開啟\n"


        page.wait_for_timeout(8000)



        codes = page.locator(
            "div.jss829"
        )


        result += (
            "jss829數量:"
            + str(codes.count())
            + "\n\n"
        )



        for i in range(min(codes.count(),60)):

            try:

                txt = codes.nth(i).inner_text().strip()

                if txt:

                    result += txt + "\n"

            except:

                pass



        body = page.locator(
            "body"
        ).inner_text()


        result += "\nDAD存在:"
        result += str("DAD" in body)



        send(result)


        browser.close()



except Exception as e:

    send(
        "錯誤:\n"+str(e)
    )
