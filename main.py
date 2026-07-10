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



        # Cookie

        try:

            page.get_by_text(
                "接受",
                exact=True
            ).click(
                timeout=3000
            )

        except:

            pass



        # =====================
        # 日期
        # =====================


        page.get_by_text(
            "出發日期",
            exact=True
        ).first.locator(
            "xpath=ancestor::div[@role='button'][1]"
        ).click()



        page.wait_for_timeout(
            2000
        )



        # 切換八月2026

        while True:

            month = page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text()


            print(
                "目前月份:",
                month
            )


            if month == "八月 2026":

                break



            page.locator(
                "button.rdrNextButton"
            ).first.evaluate(
                """
                el=>{
                    el.click();
                }
                """
            )


            page.wait_for_timeout(
                800
            )



        # 出發 15

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="15":

                days.nth(i).evaluate(
                    """
                    el=>{
                        el.click();
                    }
                    """
                )

                break



        page.wait_for_timeout(
            1500
        )



        # 回程22

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="22":

                days.nth(i).evaluate(
                    """
                    el=>{
                        el.click();
                    }
                    """
                )

                break



        page.wait_for_timeout(
            2000
        )



        # =====================
        # TPE
        # =====================


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
        ).last.evaluate(
            """
            el=>{
                el.click();
            }
            """
        )


        page.wait_for_timeout(
            2000
        )



        # =====================
        # CTS
        # =====================


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
        ).last.evaluate(
            """
            el=>{
                el.click();
            }
            """
        )


        page.wait_for_timeout(
            3000
        )



        # =====================
        # 查詢
        # =====================


        btn = page.get_by_role(
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
            "第一次查詢"
        )



        # 等跳轉

        try:

            page.wait_for_url(
                "**/select-flight**",
                timeout=30000
            )


        except:


            print(
                "第一次沒有跳轉，再試一次"
            )


            page.wait_for_timeout(
                3000
            )


            btn.evaluate(
                """
                el=>{
                    el.click();
                }
                """
            )


            page.wait_for_url(
                "**/select-flight**",
                timeout=30000
            )



        page.wait_for_load_state(
            "networkidle",
            timeout=30000
        )



        if "select-flight" in page.url:


            body = page.locator(
                "body"
            ).inner_text()



            send(
                "✅ CTS航班頁成功\n\n"
                "URL:\n"
                +page.url
                +
                "\n\nBODY:\n"
                +body[:2500]
            )


        else:


            send(
                "⚠️ 未進入航班頁\n\n"
                +page.url
            )



    except Exception as e:


        try:

            page.screenshot(
                path="error.png",
                full_page=True
            )

        except:

            pass



        send(
            "❌ 查詢異常\n\n"
            +str(e)
            +
            "\n\n"
            +
            traceback.format_exc()[-2000:]
        )



    finally:


        browser.close()
