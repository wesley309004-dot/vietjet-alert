from playwright.sync_api import sync_playwright, TimeoutError
import os
import requests
import time


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



def click_text(page, text):

    try:
        page.get_by_text(
            text,
            exact=True
        ).first.click(
            timeout=5000
        )
        return True

    except:
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


        page.wait_for_timeout(8000)



        # cookie

        click_text(
            page,
            "接受"
        )



        # 日期

        page.get_by_text(
            "出發日期",
            exact=True
        ).first.locator(
            "xpath=ancestor::div[@role='button'][1]"
        ).click()


        page.wait_for_timeout(2000)



        # 月份切換

        while True:

            month = page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text()


            if month == "八月 2026":
                break


            page.locator(
                "button.rdrNextButton"
            ).first.click()


            page.wait_for_timeout(
                500
            )



        # 8/15

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="15":

                days.nth(i).click()
                break



        page.wait_for_timeout(1000)



        # 8/22

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="22":

                days.nth(i).click()
                break



        page.wait_for_timeout(2000)



        # TPE

        inputs = page.locator(
            "input"
        )


        inputs.nth(2).fill(
            "TPE"
        )


        page.wait_for_timeout(
            2000
        )


        page.get_by_text(
            "TPE",
            exact=False
        ).last.click(
            timeout=5000
        )



        page.wait_for_timeout(
            2000
        )



        # CTS

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
            timeout=5000
        )


        page.wait_for_timeout(
            3000
        )



        before = page.url



        # 查詢

        page.get_by_role(
            "button",
            name="查詢航班"
        ).first.click(
            force=True,
            timeout=10000
        )



        # 等待跳頁

        try:

            page.wait_for_url(
                "**/select-flight**",
                timeout=30000
            )

        except:

            pass



        page.wait_for_timeout(
            10000
        )



        url = page.url



        if "select-flight" in url:


            send(
                "✅ 越捷 CTS 成功進入航班頁\n\n"
                + url
            )


        else:


            body = page.locator(
                "body"
            ).inner_text()


            send(
                "⚠️ 未進入航班頁\n\n"
                "URL:\n"
                + url
                +
                "\n\nBODY:\n"
                +
                body[:1000]
            )



    except Exception as e:


        try:

            body = page.locator(
                "body"
            ).inner_text()

        except:

            body=""


        send(
            "❌ ERROR\n\n"
            + str(e)
            +
            "\n\nURL:\n"
            +
            page.url
            +
            "\n\n"
            +
            body[:1000]
        )



    finally:

        browser.close()
