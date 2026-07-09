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



def find_code(page, code):

    items = page.locator(
        "div.jss829"
    )


    for i in range(items.count()):

        try:

            if items.nth(i).inner_text().strip() == code:

                return items.nth(i)

        except:

            pass


    return None



try:

    result="=== TPE修正版 ===\n\n"


    with sync_playwright() as p:


        browser=p.chromium.launch(
            headless=True
        )


        page=browser.new_page(
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



        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True
        )


        page.wait_for_timeout(5000)



        # 先找台灣

        taiwan = page.get_by_text(
            "台灣 (6)",
            exact=True
        )


        result += (
            "台灣數量:"
            + str(taiwan.count())
            + "\n"
        )


        if taiwan.count():

            real_click(
                page,
                taiwan
            )

            result+="展開台灣\n"


        page.wait_for_timeout(5000)



        tpe=find_code(
            page,
            "TPE"
        )


        if tpe:

            result+="找到TPE\n"

            real_click(
                page,
                tpe
            )

            result+="TPE點擊完成\n"

        else:

            result+="還是找不到TPE\n"



        send(result)


        browser.close()



except Exception as e:

    send(
        "錯誤:\n"+str(e)
    )
