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

        print(name, "click成功")
        return True


    except Exception as e:

        print(name, "普通失敗", e)


        try:

            locator.click(
                force=True,
                timeout=5000
            )

            print(name, "force成功")
            return True


        except Exception as e2:

            print(name, "失敗", e2)
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



        # 切到八月2026

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



        # 出發 8/15

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="15":

                days.nth(i).click()
                print("8/15完成")
                break



        page.wait_for_timeout(
            1000
        )



        # 回程 8/22

        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        for i in range(days.count()):

            if days.nth(i).inner_text()=="22":

                days.nth(i).click()
                print("8/22完成")
                break



        page.wait_for_timeout(
            2000
        )



        # 出發 TPE

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



        # 目的地 CTS 新千歲

        page.locator(
            "#arrivalPlaceDesktop"
        ).fill(
            "CTS"
        )


        page.wait_for_timeout(
            3000
        )



        print(
            "CTS搜尋結果:"
        )


        print(
            page.locator("body").inner_text()[:2000]
        )



        safe_click(
            page.get_by_text(
                "CTS",
                exact=False
            ).last,
            "CTS"
        )



        page.wait_for_timeout(
            2000
        )



        print(
            "CTS選取完成"
        )



        # 查詢

        page.keyboard.press(
            "Escape"
        )


        page.wait_for_timeout(
            2000
        )


        btn = page.get_by_role(
            "button",
            name="查詢航班"
        ).first


        safe_click(
            btn,
            "查詢航班"
        )


        page.wait_for_timeout(
            10000
        )


        send(
            "CTS札幌新千歲測試完成"
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
