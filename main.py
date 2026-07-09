import os
import requests
from playwright.sync_api import sync_playwright


FROM = "TPE"
TO = "DAD"

GO_DATE = "2026-10-20"
RETURN_DATE = "2026-10-24"

DEBUG = True


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



def log(text):

    print(text)

    if DEBUG:
        send(text)



def screenshot(page,name):

    try:
        page.screenshot(
            path=name+".png",
            full_page=True
        )
    except:
        pass



def mouse_click(page, locator):

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



def open_page(page):

    log("🌐 開啟網站")


    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000
    )


    page.wait_for_timeout(10000)



def accept_cookie(page):

    try:

        page.get_by_text(
            "接受",
            exact=True
        ).click(
            timeout=5000
        )

        log("🍪 Cookie完成")

    except:

        pass



def select_departure(page):

    log("🛫 TPE")


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
        "div"
    ).filter(
        has_text="臺北"
    ).filter(
        has_text="TPE"
    ).filter(
        has_text="桃園國際機場"
    ).first



    mouse_click(
        page,
        tpe
    )


    page.wait_for_timeout(5000)


    log("✅ TPE完成")



def select_destination(page):

    log("🛬 DAD")


    page.get_by_text(
        "目的地",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(8000)



    dad = page.get_by_text(
        TO,
        exact=True
    ).last


    mouse_click(
        page,
        dad
    )


    page.wait_for_timeout(5000)


    log("✅ DAD完成")



def choose_day(page,date,label):

    day = date.split("-")[2]


    target = page.get_by_text(
        str(int(day)),
        exact=True
    ).last


    mouse_click(
        page,
        target
    )


    page.wait_for_timeout(3000)


    log(
        f"✅ {label}"
    )



def select_date(page):

    page.get_by_text(
        "出發日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)


    choose_day(
        page,
        GO_DATE,
        GO_DATE
    )



def select_return_date(page):

    page.get_by_text(
        "返程日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)


    choose_day(
        page,
        RETURN_DATE,
        RETURN_DATE
    )



# ===============================
# 新增：查詢按鈕Debug
# ===============================

def debug_before_search(page):

    log("🔎 查詢前檢查")


    body = page.locator(
        "body"
    ).inner_text()



    send(
        "查詢前文字:\n\n"
        +
        body[:1500]
    )



    buttons = page.locator(
        "button"
    )


    send(
        "button數量:"
        +
        str(buttons.count())
    )



    for i in range(min(buttons.count(),20)):

        try:

            txt = buttons.nth(i).inner_text()

            if txt.strip():

                send(
                    f"button {i}:\n{txt[:100]}"
                )

        except:

            pass



def click_search(page):

    log("🔍 找查詢按鈕")


    debug_before_search(page)



    buttons = page.locator(
        "button"
    )


    found = False



    for i in range(buttons.count()):

        try:

            txt = buttons.nth(i).inner_text()


            if "查詢航班" in txt:


                send(
                    "找到button:\n"
                    +
                    txt
                )


                buttons.nth(i).click(
                    force=True
                )


                found = True

                break


        except:

            pass



    if not found:

        raise Exception(
            "找不到查詢button"
        )



    log(
        "✅ 已點查詢"
    )



    page.wait_for_timeout(
        30000
    )



    send(
        "目前URL:\n"
        +
        page.url
    )



    screenshot(
        page,
        "after_click"
    )



def main():

    send(
        "🚀 查詢按鈕DOM Debug"
    )


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )



        try:

            open_page(page)

            accept_cookie(page)

            select_departure(page)

            select_destination(page)

            select_date(page)

            select_return_date(page)

            click_search(page)


            send(
                "🎉 完成"
            )


        except Exception as e:


            screenshot(
                page,
                "error"
            )


            send(
                "❌錯誤\n"
                +
                str(e)
            )


        finally:

            browser.close()



if __name__=="__main__":

    main()
