from playwright.sync_api import sync_playwright
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



        try:

            page.get_by_text(
                "接受",
                exact=True
            ).click(
                timeout=3000
            )

        except:
            pass



        # 開日期

        page.get_by_text(
            "出發日期",
            exact=True
        ).first.locator(
            "xpath=ancestor::div[@role='button'][1]"
        ).click()



        page.wait_for_timeout(2000)



        # 八月

        while True:

            m=page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text()


            if m=="八月 2026":
                break


            page.locator(
                "button.rdrNextButton"
            ).first.click()


            page.wait_for_timeout(500)



        # 15

        for i in range(
            page.locator(".rdrDay:not(.rdrDayPassive)").count()
        ):

            d=page.locator(
                ".rdrDay:not(.rdrDayPassive)"
            ).nth(i)


            if d.inner_text()=="15":

                d.click()
                break



        page.wait_for_timeout(1000)



        # 22

        for i in range(
            page.locator(".rdrDay:not(.rdrDayPassive)").count()
        ):

            d=page.locator(
                ".rdrDay:not(.rdrDayPassive)"
            ).nth(i)


            if d.inner_text()=="22":

                d.click()
                break



        page.wait_for_timeout(1000)



        # TPE

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



        # =========================
        # 真正提交
        # =========================


        buttons=page.locator(
            "button"
        )


        target=None


        for i in range(buttons.count()):

            txt=buttons.nth(i).inner_text()


            if txt.strip()=="查詢航班":

                target=buttons.nth(i)
                break



        if target:


            target.scroll_into_view_if_needed()


            page.wait_for_timeout(1000)



            target.evaluate(
                """
                el=>{
                    el.click();
                }
                """
            )


        else:


            raise Exception(
                "找不到查詢按鈕"
            )



        # 等 React routing

        page.wait_for_timeout(
            15000
        )



        if "/select-flight" in page.url:


            send(
                "✅ CTS進入航班頁\n\n"
                +page.url
            )


        else:


            send(
                "⚠️ 還在首頁\n\nURL:\n"
                +page.url
                +"\n\n"
                +page.locator("body").inner_text()[:2000]
            )



    except Exception as e:


        send(
            "❌ ERROR\n\n"
            +str(e)
        )



    finally:

        browser.close()
