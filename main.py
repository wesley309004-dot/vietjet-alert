from playwright.sync_api import sync_playwright, TimeoutError
import os
import requests
import traceback


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(msg):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg[:4000]
        },
        timeout=20
    )



def safe_click(locator, name):

    try:
        locator.scroll_into_view_if_needed()

        locator.click(
            timeout=10000,
            force=True
        )

        print(name,"完成")

        return True

    except Exception as e:

        print(
            name,
            "失敗",
            e
        )

        return False



with sync_playwright() as p:


    browser = p.chromium.launch(
        headless=True
    )


    page = browser.new_page(
        locale="zh-TW"
    )


    try:


        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        page.wait_for_timeout(
            8000
        )


        # cookie

        try:

            page.get_by_text(
                "接受",
                exact=True
            ).click(
                timeout=3000
            )

        except:

            pass



        # 日期

        page.get_by_text(
            "出發日期",
            exact=True
        ).first.locator(
            "xpath=ancestor::div[@role='button'][1]"
        ).click()



        page.wait_for_timeout(
            2000
        )



        # 切八月2026

        while True:


            month = page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text()


            print(
                "月份:",
                month
            )


            if month == "八月 2026":

                break



            page.locator(
                "button.rdrNextButton"
            ).first.click(
                force=True
            )


            page.wait_for_timeout(
                500
            )



        # 出發15

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="15":

                days.nth(i).click(
                    force=True
                )

                break



        page.wait_for_timeout(
            1000
        )



        # 回程22

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="22":

                days.nth(i).click(
                    force=True
                )

                break



        page.wait_for_timeout(
            2000
        )



        # 出發地 TPE

        page.locator(
            "input"
        ).nth(2).fill(
            "TPE"
        )


        page.wait_for_timeout(
            2000
        )


        page.get_by_text(
            "TPE",
            exact=False
        ).last.click(
            force=True
        )



        page.wait_for_timeout(
            2000
        )



        # 目的地 CTS

        page.locator(
            "#arrivalPlaceDesktop"
        ).fill(
            "CTS"
        )


        page.wait_for_timeout(
            2000
        )


        page.get_by_text(
            "CTS",
            exact=False
        ).last.click(
            force=True
        )


        print(
            "CTS完成"
        )



        page.wait_for_timeout(
            3000
        )



        # 查詢

        safe_click(
            page.get_by_role(
                "button",
                name="查詢航班"
            ).first,
            "查詢"
        )



        # 等結果

        page.wait_for_timeout(
            15000
        )



        url = page.url


        body = page.locator(
            "body"
        ).inner_text()



        if "select-flight" in url:


            msg = f"""
✅ 越捷CTS找到查詢頁

URL:
{url}

BODY:

{body[:2500]}
"""


            send(msg)



        else:


            msg = f"""
⚠️ 未進入航班頁

URL:
{url}

BODY:

{body[:2000]}
"""


            send(msg)



    except Exception as e:


        send(
            "❌ 查詢異常\n\n"
            + str(e)
            + "\n\n"
            + traceback.format_exc()[-2000:]
        )


    finally:


        browser.close()
