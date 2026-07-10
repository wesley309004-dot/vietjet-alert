from playwright.sync_api import sync_playwright, TimeoutError
import os
import requests


TOKEN=os.environ["TELEGRAM_TOKEN"]
CHAT_ID=os.environ["TELEGRAM_CHAT_ID"]


def send(msg):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id":CHAT_ID,
            "text":msg[:4000]
        },
        timeout=20
    )



with sync_playwright() as p:


    browser=p.chromium.launch(
        headless=True
    )


    page=browser.new_page(
        locale="zh-TW"
    )


    try:

        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        page.wait_for_timeout(8000)



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


        page.wait_for_timeout(2000)



        # 到八月

        while True:

            month=page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text()


            if month=="八月 2026":
                break


            page.locator(
                "button.rdrNextButton"
            ).first.click()


            page.wait_for_timeout(500)



        days=page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="15":

                days.nth(i).click()
                break



        page.wait_for_timeout(1000)



        days=page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="22":

                days.nth(i).click()
                break



        page.wait_for_timeout(1000)



        # 出發 TPE

        page.locator(
            "input"
        ).nth(2).fill(
            "TPE"
        )


        page.wait_for_timeout(2000)


        page.get_by_text(
            "TPE",
            exact=False
        ).last.click()



        page.wait_for_timeout(1000)



        # CTS

        page.locator(
            "#arrivalPlaceDesktop"
        ).fill(
            "CTS"
        )


        page.wait_for_timeout(2000)


        page.get_by_text(
            "CTS",
            exact=False
        ).last.click()



        page.wait_for_timeout(2000)



        # =====================
        # 查詢
        # =====================


        btn=page.get_by_role(
            "button",
            name="查詢航班"
        ).first


        btn.scroll_into_view_if_needed()


        page.wait_for_timeout(1000)


        try:

            btn.click(
                force=True,
                timeout=10000
            )

        except:


            page.keyboard.press(
                "Enter"
            )



        # 等待跳頁

        try:

            page.wait_for_url(
                "**/select-flight**",
                timeout=30000
            )


            send(
                "✅ CTS進入航班頁\n\nURL:\n"+page.url
            )


        except:


            send(
                "⚠️ 未進入航班頁\n\nURL:\n"
                +page.url
                +"\n\nBODY:\n"
                +page.locator("body").inner_text()[:3000]
            )



    except Exception as e:


        send(
            "❌ ERROR\n\n"
            +str(e)
        )



    finally:

        browser.close()
