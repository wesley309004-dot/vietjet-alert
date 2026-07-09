import os
import time
import requests
from playwright.sync_api import sync_playwright, TimeoutError


# =========================
# 設定區
# =========================

FROM = "TPE"
TO = "DAD"

DEBUG = True


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


# =========================
# Telegram
# =========================

def send(text):

    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=20
        )

    except Exception as e:
        print(e)



# =========================
# 工具
# =========================

def log(msg):

    print(msg)

    if DEBUG:
        send(msg)



def screenshot(page, name):

    try:
        page.screenshot(
            path=f"{name}.png",
            full_page=True
        )

    except:
        pass



def mouse_click(page, locator):

    box = locator.bounding_box()

    if not box:
        return False


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



# =========================
# 開首頁
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
# 選出發地
# =========================

def select_departure(page):

    log("🛫 開啟出發地")


    page.get_by_text(
        "出發地點",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)



    # 展開台灣

    try:

        page.get_by_text(
            "台灣 (6)",
            exact=True
        ).click(
            force=True
        )


        log("🇹🇼 展開台灣")


    except:

        log("⚠️ 找不到台灣分類")



    page.wait_for_timeout(5000)



    # 不用jss
    # 用完整文字區塊

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

        screenshot(
            page,
            "error_departure"
        )

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
# 選目的地
# =========================

def select_destination(page):

    log("🛬 開啟目的地")


    page.get_by_text(
        "目的地",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(8000)



    # 不用class
    dad = page.get_by_text(
        TO,
        exact=True
    ).last



    if dad.count() == 0:

        screenshot(
            page,
            "error_destination"
        )

        raise Exception(
            f"找不到{TO}"
        )



    mouse_click(
        page,
        dad
    )


    page.wait_for_timeout(5000)


    log(
        f"✅ {TO}完成"
    )



# =========================
# 主程式
# =========================

def main():


    send(
        "🚀 Vietjet監控開始"
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


            screenshot(
                page,
                "success_airport"
            )


            send(
                "🎉 出發地+目的地完成"
            )



        except Exception as e:


            send(
                "❌錯誤\n"
                + str(e)
            )


            screenshot(
                page,
                "error_final"
            )



        finally:

            browser.close()



if __name__ == "__main__":

    main()
