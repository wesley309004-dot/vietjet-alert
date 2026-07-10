from playwright.sync_api import sync_playwright
import os
import requests
import traceback


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



        while True:

            m=page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text()


            if m=="八月 2026":

                break


            page.locator(
                "button.rdrNextButton"
            ).first.click(
                force=True
            )

            page.wait_for_timeout(500)



        # 15

        for i in range(
            page.locator(
                ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
            ).count()
        ):

            d=page.locator(
                ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
            ).nth(i)


            if d.inner_text()=="15":

                d.click(force=True)
                break



        page.wait_for_timeout(1000)



        # 22

        for i in range(
            page.locator(
                ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
            ).count()
        ):

            d=page.locator(
                ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
            ).nth(i)


            if d.inner_text()=="22":

                d.click(force=True)
                break



        page.wait_for_timeout(1500)



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
        ).last.click(
            force=True
        )



        page.wait_for_timeout(1500)



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
        ).last.click(
            force=True
        )



        page.wait_for_timeout(3000)



        # =====================
        # React 真正提交
        # =====================


        btn=page.get_by_role(
            "button",
            name="查詢航班"
        ).first



        btn.evaluate(
            """
            el=>{
                el.click();
            }
            """
        )



        print(
            "已觸發React click"
        )



        page.wait_for_timeout(
            15000
        )



        if "select-flight" in page.url:


            send(
                "✅ CTS成功\n\n"
                +page.url
            )


        else:


            send(
                "⚠️ 仍在首頁\n\n"
                +page.url
            )



    except Exception as e:


        send(
            "❌ ERROR\n\n"
            +str(e)
            +"\n\n"
            +traceback.format_exc()[-1500:]
        )


    finally:

        browser.close()
