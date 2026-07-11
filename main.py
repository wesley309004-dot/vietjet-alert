from playwright.sync_api import sync_playwright, TimeoutError
import os
import requests
import traceback
import datetime
import time

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send(msg):

    try:

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": msg[:4000]
            },
            timeout=20
        )

    except Exception as e:

        print(
            "Telegram error:",
            e
        )

def debug(msg):

    print(
        datetime.datetime.now(),
        msg
    )

def wait(page, sec=1):

    page.wait_for_timeout(
        sec * 1000
    ) def open_vietjet(page):

    debug("開啟越捷首頁")

    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000
    )

    wait(
        page,
        8
    )

    try:

        page.get_by_text(
            "接受",
            exact=True
        ).click(
            timeout=3000
        )

        debug(
            "Cookie 已接受"
        )

    except:

        debug(
            "沒有 Cookie"
        )

def select_date(page):

    debug(
        "開啟日期選擇"
    )

    page.get_by_text(
        "出發日期",
        exact=True
    ).first.locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click()

    wait(
        page,
        2
    )

    # 目前測試日期
    # 2026/08/15 - 2026/08/22

    while True:

        month = page.locator(
            ".rdrMonthAndYearPickers"
        ).first.inner_text()

        debug(
            "目前月份:"+month
        )

        if month == "八月 2026":

            break

        page.locator(
            "button.rdrNextButton"
        ).first.click(
            force=True
        )

        wait(
            page,
            1
        )

    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )

    for i in range(days.count()):

        if days.nth(i).inner_text()=="15":

            days.nth(i).click(
                force=True
            )

            debug(
                "出發日期完成"
            )

            break

    wait(
        page,
        2
    )

    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )

    for i in range(days.count()):

        if days.nth(i).inner_text()=="22":

            days.nth(i).click(
                force=True
            )

            debug(
                "回程日期完成"
            )

            break

    wait(
        page,
        2
    )

def select_airport(page, input_id, code):

    debug(
        f"選擇機場 {code}"
    )

    box = page.locator(
        input_id
    )

    box.click(
        force=True
    )

    box.fill(
        code
    )

    wait(
        page,
        3
    )

    try:

        page.get_by_text(
            code,
            exact=False
        ).last.click(
            force=True,
            timeout=10000
        )

        debug(
            f"{code} 選取成功"
        )

    except Exception as e:

        debug(
            f"{code} 選取失敗 {e}"
        )

        raise

def search_flight(page):

    debug(
        "準備查詢航班"
    )

    try:

        button = page.get_by_role(
            "button",
            name="查詢航班"
        ).first

        button.click(
            force=True,
            timeout=10000
        )

    except Exception as e:

        debug(
            "查詢按鈕失敗"
        )

        raise e

    wait(
        page,
        10
    )

    debug(
        "目前網址:"
        + page.url
    )

    if "select-flight" in page.url:

        debug(
            "成功進入航班頁"
        )

        return True

    else:

        debug(
            "沒有進入航班頁"
        )

        return False

def main():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            locale="zh-TW"
        )

        try:

            open_vietjet(
                page
            )

            select_date(
                page
            )

            # 出發地
            select_airport(
                page,
                "#departPlaceDesktop",
                "TPE"
            )

            wait(
                page,
                2
            )

            # 目的地
            select_airport(
                page,
                "#arrivalPlaceDesktop",
                "CTS"
            )

            wait(
                page,
                3
            )

            success = search_flight(
                page
            )

            if success:

                body = page.locator(
                    "body"
                ).inner_text(
                    timeout=10000
                )

                send(
                    "✅ CTS航班頁成功\n\n"
                    + page.url
                    + "\n\n"
                    + body[:3000]
                )

            else:

                send(
                    "⚠️ CTS未進入航班頁\n"
                    + page.url
                )

        except Exception as e:

            debug(
                traceback.format_exc()
            )

            try:

                page.screenshot(
                    path="error.png",
                    full_page=True
                )

            except:

                pass

            send(
                "❌ Vietjet錯誤\n\n"
                + str(e)
                + "\n\n"
                + traceback.format_exc()[-2000:]
            )

        finally:

            browser.close()

if __name__ == "__main__":

    main()
