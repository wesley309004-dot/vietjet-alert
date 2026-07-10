from playwright.sync_api import sync_playwright
import os
import requests


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
            "Telegram錯誤:",
            e
        )



def safe_click(locator, name=""):

    try:

        locator.click(
            timeout=5000
        )

        print(
            name,
            "click成功"
        )

        return True


    except Exception as e:

        print(
            name,
            "普通click失敗:",
            e
        )


        try:

            locator.click(
                force=True,
                timeout=5000
            )

            print(
                name,
                "force成功"
            )

            return True


        except Exception as e2:

            print(
                name,
                "失敗:",
                e2
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
            ).first.click()


            page.wait_for_timeout(
                500
            )



        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="15":

                days.nth(i).click()

                print(
                    "去程完成"
                )

                break



        page.wait_for_timeout(
            1000
        )



        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="22":

                days.nth(i).click()

                print(
                    "回程完成"
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


        safe_click(
            page.get_by_text(
                "TPE",
                exact=False
            ).last,
            "TPE"
        )


        page.wait_for_timeout(
            1000
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
            3000
        )


        safe_click(
            page.get_by_text(
                "CTS",
                exact=False
            ).last,
            "CTS"
        )


        page.wait_for_timeout(
            3000
        )


        print(
            "CTS完成"
        )



        # =====================
        # 查詢 (React JS click)
        # =====================


        page.keyboard.press(
            "Escape"
        )


        page.wait_for_timeout(
            2000
        )



        print(
            "準備查詢"
        )



        result = page.evaluate(
            """
            () => {

                const buttons =
                [...document.querySelectorAll("button")];


                const btn =
                buttons.find(
                    b =>
                    b.innerText.includes("查詢航班")
                );


                if(btn){

                    btn.click();

                    return "clicked";

                }


                return "not found";

            }
            """
        )



        print(
            "JS結果:",
            result
        )



        page.wait_for_timeout(
            20000
        )



        title = page.title()

        url = page.url

        body = page.locator(
            "body"
        ).inner_text()



        send(
            f"""
越捷CTS查詢測試

TITLE:
{title}

URL:
{url}


BODY:
{body[:3000]}
"""
        )



    except Exception as e:


        print(
            "失敗:",
            e
        )


        send(
            f"CTS測試失敗\n{e}"
        )



    finally:


        browser.close()
