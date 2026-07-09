import os
import requests
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
            "text": text
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

    log("🇹🇼 展開台灣")


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

    log("🛬 開啟目的地")


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



# ============================
# 新增：React查詢追蹤
# ============================

def setup_network(page):

    requests_log = []


    def handle(req):

        url = req.url


        if (
            "api" in url.lower()
            or "search" in url.lower()
            or "flight" in url.lower()
        ):

            requests_log.append(url)

            send(
                "🌐 Request:\n"
                + url[:300]
            )


    page.on(
        "request",
        handle
    )


    return requests_log



def click_search_debug(page, requests_log):

    log("🔍 找查詢文字")


    target = page.get_by_text(
        "查詢航班",
        exact=True
    ).last



    if target.count()==0:

        raise Exception(
            "找不到查詢航班"
        )


    html = target.evaluate(
        "(e)=>e.outerHTML"
    )


    send(
        "按鈕HTML:\n"
        +html[:1000]
    )



    parent = target.locator(
        "xpath=.."
    )


    parent_html = parent.evaluate(
        "(e)=>e.outerHTML"
    )


    send(
        "父層HTML:\n"
        +parent_html[:1500]
    )



    log("🖱 JS click")


    target.evaluate(
        "(e)=>e.click()"
    )


    page.wait_for_timeout(5000)



    log("🖱 dispatch click")


    target.dispatch_event(
        "click"
    )


    page.wait_for_timeout(30000)



    send(
        "最後URL:\n"
        +page.url
    )


    send(
        "API數量:"
        +str(len(requests_log))
    )



def main():

    send(
        "🚀 React事件Debug開始"
    )


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        try:

            requests_log = setup_network(page)


            open_page(page)

            accept_cookie(page)

            select_departure(page)

            select_destination(page)

            select_dates(page)

            click_search_debug(
                page,
                requests_log
            )


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
