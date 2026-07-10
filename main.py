from playwright.sync_api import sync_playwright
import os
import requests
from datetime import datetime


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



# ==========================
# 設定搜尋日期
# ==========================

DEPART_DATE = "15"
RETURN_DATE = "22"

TARGET_MONTH = "八月 2026"



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

        try:

            page.get_by_text(
                "接受",
                exact=True
            ).click(
                timeout=3000
            )

        except:

            pass



        # ==========================
        # 點日期
        # ==========================


        page.get_by_text(
            "出發日期",
            exact=True
        ).first.locator(
            "xpath=ancestor::div[@role='button'][1]"
        ).click()


        page.wait_for_timeout(2000)



        # ==========================
        # 月份切換
        # ==========================


        while True:


            month = page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text()


            print(
                "月份:",
                month
            )


            if month == TARGET_MONTH:

                break


            page.locator(
                "button.rdrNextButton"
            ).first.click()


            page.wait_for_timeout(500)



        # ==========================
        # 出發日
        # ==========================


        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        clicked = False


        for i in range(days.count()):


            if days.nth(i).inner_text() == DEPART_DATE:


                days.nth(i).click()

                clicked=True

                print(
                    "出發日期完成"
                )

                break



        if not clicked:

            raise Exception(
                "找不到出發日期"
            )



        page.wait_for_timeout(1000)



        # ==========================
        # 回程日
        # ==========================


        days = page.locator(
            ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
        )


        clicked=False


        for i in range(days.count()):


            if days.nth(i).inner_text()==RETURN_DATE:


                days.nth(i).click()

                clicked=True

                print(
                    "回程日期完成"
                )

                break



        if not clicked:

            raise Exception(
                "找不到回程日期"
            )



        page.wait_for_timeout(1500)



        # ==========================
        # 出發地 TPE
        # ==========================


        inputs = page.locator(
            "input"
        )


        inputs.nth(2).fill(
            "TPE"
        )


        page.wait_for_timeout(2000)



        page.get_by_text(
            "TPE",
            exact=False
        ).last.click(
            timeout=5000
        )


        print(
            "TPE完成"
        )



        # ==========================
        # CTS
        # ==========================


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
            timeout=5000
        )


        print(
            "CTS完成"
        )



        page.wait_for_timeout(2000)



        # ==========================
        # 查詢按鈕
        # ==========================


        btn = page.get_by_role(
            "button",
            name="查詢航班"
        ).first



        btn.click(
            force=True
        )


        print(
            "送出查詢"
        )



        page.wait_for_timeout(
            15000
        )



        url = page.url

        body = page.locator(
            "body"
        ).inner_text()



        # ==========================
        # 判斷
        # ==========================


        if "/select-flight" in url:


            if "找不到適合您選擇的航班" in body:


                msg=f"""
❌ 越捷 CTS 無航班

TPE → CTS

日期:
{DEPART_DATE}/{TARGET_MONTH}

URL:
{url}
"""


            else:


                msg=f"""
🎉 越捷 CTS 發現航班！

TPE → CTS

日期:
{DEPART_DATE}/{TARGET_MONTH}

URL:
{url}
"""



        else:


            msg="""
⚠️ 查詢異常
未進入航班頁
"""


        send(msg)



    except Exception as e:


        send(
            "❌ 執行錯誤\n\n"
            + str(e)
        )


    finally:


        browser.close()
