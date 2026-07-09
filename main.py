import os
import requests
import json
from playwright.sync_api import sync_playwright


FROM = "TPE"
TO = "DAD"

GO_DATE = "2026-10-20"
RETURN_DATE = "2026-10-24"


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]



def send(text):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text[:4000]
        },
        timeout=20
    )



def log(text):

    print(text)
    send(text)



def mouse_click(page, locator):

    box = locator.bounding_box()

    if not box:
        return False


    page.mouse.click(
        box["x"] + box["width"]/2,
        box["y"] + box["height"]/2
    )

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

        pass



def select_departure(page):

    log("🇹🇼 TPE")


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



def choose_day(page,date):

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



def select_dates(page):

    log("📅 日期")


    page.get_by_text(
        "出發日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)


    choose_day(
        page,
        GO_DATE
    )


    page.get_by_text(
        "返程日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)


    choose_day(
        page,
        RETURN_DATE
    )


    log("✅ 日期完成")



# ==========================
# API Response監控
# ==========================

api_result = []


def setup_response(page):


    def response_handler(res):

        url = res.url.lower()


        if (
            "api" in url
            or "flight" in url
            or "search" in url
            or "booking" in url
        ):


            status = res.status


            item = {
                "status": status,
                "url": res.url
            }


            try:

                data = res.text()

                item["body"] = data[:500]


            except:

                pass



            api_result.append(item)



    page.on(
        "response",
        response_handler
    )



def click_search(page):

    log("🔍 點查詢")


    btn = page.get_by_text(
        "查詢航班",
        exact=True
    ).last


    btn.evaluate(
        "(e)=>e.click()"
    )


    page.wait_for_timeout(
        30000
    )


    log("📡 API整理")



    output = []


    for x in api_result:


        # 只看重要的

        if (
            x["status"] != 200
            or
            "flight" in x["url"].lower()
            or
            "search" in x["url"].lower()
        ):


            output.append(
                "STATUS:\n"
                +str(x["status"])
                +
                "\nURL:\n"
                +x["url"][:300]
                +
                "\nBODY:\n"
                +x.get("body","")[:500]
            )



    if len(output)==0:

        send(
            "沒有抓到搜尋API"
        )

    else:

        send(
            "\n\n==========\n\n".join(
                output[:10]
            )
        )



    send(
        "最後URL:\n"
        +page.url
    )



def main():

    send(
        "🚀 API Response Debug開始"
    )


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        try:

            setup_response(page)


            open_page(page)

            accept_cookie(page)

            select_departure(page)

            select_destination(page)

            select_dates(page)

            click_search(page)


            send(
                "🎉完成"
            )


        except Exception as e:

            send(
                "❌錯誤\n"+str(e)
            )


        finally:

            browser.close()



if __name__=="__main__":

    main()
