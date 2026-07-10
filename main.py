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
        print("Telegram失敗:", e)



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
            "普通click失敗",
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
                "失敗",
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



        # =====================
        # 日期
        # =====================


        date_btn = page.get_by_text(
            "出發日期",
            exact=True
        ).first.locator(
            "xpath=ancestor::div[@role='button'][1]"
        )


        safe_click(
            date_btn,
            "日期"
        )


        page.wait_for_timeout(
            2000
        )



        # =====================
        # 切八月2026
        # =====================


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
            ).first.click()


            page.wait_for_timeout(
                500
            )



        print(
            "八月到達"
        )



        # =====================
        # 出發8/15
        # =====================


        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        found = False


        for i in range(days.count()):

            if days.nth(i).inner_text() == "15":

                days.nth(i).click()

                found = True

                print(
                    "出發8/15完成"
                )

                break


        if not found:

            raise Exception(
                "找不到8/15"
            )



        page.wait_for_timeout(
            1000
        )



        # =====================
        # 回程8/22
        # =====================


        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        found = False


        for i in range(days.count()):

            if days.nth(i).inner_text() == "22":

                days.nth(i).click()

                found = True

                print(
                    "回程8/22完成"
                )

                break


        if not found:

            raise Exception(
                "找不到8/22"
            )



        page.wait_for_timeout(
            2000
        )



        # =====================
        # 出發地 TPE
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
        # 目的地 PQC
        # =====================


        page.locator(
            "#arrivalPlaceDesktop"
        ).fill(
            "PQC"
        )


        page.wait_for_timeout(
            2000
        )


        safe_click(
            page.get_by_text(
                "PQC",
                exact=False
            ).last,
            "PQC"
        )



        page.wait_for_timeout(
            2000
        )



        print(
            "TPE PQC選取成功"
        )



        # =====================
        # 查詢
        # =====================


        try:

            page.keyboard.press(
                "Escape"
            )


        except:

            pass



        page.wait_for_timeout(
            2000
        )



        btns = page.get_by_role(
            "button",
            name="查詢航班"
        )


        print(
            "查詢按鈕數:",
            btns.count()
        )


        search_btn = btns.first


        search_btn.scroll_into_view_if_needed()



        if not safe_click(
            search_btn,
            "查詢航班"
        ):

            raise Exception(
                "查詢按鈕點擊失敗"
            )



        page.wait_for_timeout(
            10000
        )



        send(
            "越捷查詢完成"
        )



    except Exception as e:


        print(
            "程式失敗:",
            e
        )


        send(
            f"程式失敗\n{e}"
        )



    finally:


        browser.close()
