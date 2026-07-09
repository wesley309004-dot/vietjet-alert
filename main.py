import os
import re
import requests
from playwright.sync_api import sync_playwright


# =========================
# 設定
# =========================

FROM = "TPE"
TO = "DAD"

# 夏季航班測試日期
GO_DATE = "2026-10-20"
RETURN_DATE = "2026-10-24"

DEBUG = True


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]



# =========================
# Telegram
# =========================

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



# =========================
# 工具
# =========================

def mouse_click(page, locator):

    box = locator.bounding_box()

    if not box:
        return False


    x = box["x"] + box["width"] / 2
    y = box["y"] + box["height"] / 2


    page.mouse.move(x, y)
    page.mouse.down()

    page.wait_for_timeout(200)

    page.mouse.up()

    return True



def screenshot(page, name):

    try:

        page.screenshot(
            path=name + ".png",
            full_page=True
        )

    except:

        pass



# =========================
# 首頁
# =========================

def open_page(page):

    log("🌐 開啟 Vietjet")


    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000
    )


    page.wait_for_timeout(10000)



# =========================
# Cookie
# =========================

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



# =========================
# 出發地
# =========================

def select_departure(page):

    log("🛫 選擇出發地")


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



    if tpe.count() == 0:

        raise Exception(
            "找不到TPE"
        )


    mouse_click(
        page,
        tpe
    )


    page.wait_for_timeout(5000)


    log("✅ TPE完成")



# =========================
# 目的地
# =========================

def select_destination(page):

    log("🛬 選擇目的地")


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



    if dad.count() == 0:

        raise Exception(
            "找不到DAD"
        )


    mouse_click(
        page,
        dad
    )


    page.wait_for_timeout(5000)


    log("✅ DAD完成")



# =========================
# 日期
# =========================

def choose_day(page, date_value, title):

    day = date_value.split("-")[2]


    target = page.get_by_text(
        str(int(day)),
        exact=True
    ).last



    if target.count() == 0:

        raise Exception(
            f"找不到日期 {date_value}"
        )


    mouse_click(
        page,
        target
    )


    page.wait_for_timeout(3000)


    log(
        f"✅ {title} {date_value}"
    )



def select_date(page):

    log("📅 去程日期")


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

    log("📅 回程日期")


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



# =========================
# 查詢
# =========================

def search_flight(page):

    log("🔍 查詢航班")


    page.get_by_text(
        "查詢航班",
        exact=True
    ).click(
        force=True
    )


    log(
        "⏳ 等待結果頁"
    )


    page.wait_for_timeout(30000)


    log(
        "✅ 查詢完成"
    )



# =========================
# 結果頁 Debug
# =========================

def debug_result(page):

    log("📄 分析結果頁")


    url = page.url


    send(
        "目前網址:\n" + url
    )



    body = page.locator(
        "body"
    ).inner_text()



    keywords = [
        "TWD",
        "HKD",
        "USD",
        "價格",
        "航班",
        "Vietjet",
        "選擇"
    ]



    found = []


    for k in keywords:

        if k in body:

            found.append(k)



    send(
        "找到關鍵字:\n"
        +
        "\n".join(found)
    )



    prices = re.findall(
        r"\b\d{3,6}\b",
        body
    )


    unique = []


    for p in prices:

        if p not in unique:

            unique.append(p)



    send(
        "數字候選:\n"
        +
        "\n".join(unique[:50])
    )


    screenshot(
        page,
        "result_debug"
    )



# =========================
# 主程式
# =========================

def main():

    send(
        "🚀 Vietjet夏季航班Debug開始"
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

            debug_result(page)


            send(
                "🎉 結果頁分析完成"
            )



        except Exception as e:


            screenshot(
                page,
                "error"
            )


            send(
                "❌錯誤\n"
                + str(e)
            )



        finally:

            browser.close()



if __name__ == "__main__":

    main()
