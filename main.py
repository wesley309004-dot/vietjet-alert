import os
import requests
import time
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

    log("🌐 開啟 Vietjet")

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

        log("🍪 無Cookie")



def select_departure(page):

    log("🛫 選擇TPE")


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

    log("🛬 選擇DAD")


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
        f"✅ {label} {date}"
    )



def select_date(page):

    log("📅 去程")

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
        "去程"
    )



def select_return_date(page):

    log("📅 回程")

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
        "回程"
    )



def check_form(page):

    text = page.locator(
        "body"
    ).inner_text()


    result = []


    for key in [
        "TPE",
        "DAD",
        GO_DATE.split("-")[2],
        RETURN_DATE.split("-")[2]
    ]:

        if key in text:

            result.append(
                key+" OK"
            )

        else:

            result.append(
                key+" missing"
            )


    send(
        "📝表單檢查\n\n"
        +
        "\n".join(result)
    )



def search_flight(page):

    log("🔍準備查詢")


    check_form(page)


    old_url = page.url



    # 方法1

    try:

        page.get_by_text(
            "查詢航班",
            exact=True
        ).click(
            force=True
        )

        log("點擊文字按鈕")

    except:

        pass



    page.wait_for_timeout(5000)



    # 方法2

    try:

        page.locator(
            "button"
        ).filter(
            has_text="查詢航班"
        ).click(
            force=True
        )

        log("點擊button")

    except:

        pass



    # 方法3

    try:

        page.keyboard.press(
            "Enter"
        )

        log("Enter提交")

    except:

        pass



    for i in range(1,7):

        page.wait_for_timeout(5000)


        now = page.url


        text = page.locator(
            "body"
        ).inner_text()


        send(
            f"⏱ {i*5}秒\n"
            f"URL:\n{now}\n\n"
            f"包含航班:{'航班' in text}\n"
            f"包含TWD:{'TWD' in text}"
        )


        if now != old_url:

            log("🎯 URL已變更")
            break



def main():

    send(
        "🚀 查詢提交Debug開始"
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

            search_flight(page)


            screenshot(
                page,
                "after_search"
            )


            send(
                "🎉 Debug完成"
            )


        except Exception as e:


            screenshot(
                page,
                "error"
            )


            send(
                "❌錯誤\n"+str(e)
            )


        finally:

            browser.close()



if __name__=="__main__":

    main()
