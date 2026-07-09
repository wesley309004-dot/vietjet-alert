from playwright.sync_api import sync_playwright
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



with sync_playwright() as p:


    browser = p.chromium.launch(
        headless=True
    )


    page = browser.new_page(
        locale="zh-TW"
    )


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



    # =====================
    # 點日期
    # =====================


    page.get_by_text(
        "出發日期",
        exact=True
    ).first.locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click()


    page.wait_for_timeout(2000)



    # =====================
    # 切換到八月2026
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


        page.wait_for_timeout(500)



    print(
        "到達八月"
    )



    # =====================
    # 選出發日期 15
    # =====================


    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):


        if days.nth(i).inner_text()=="15":


            days.nth(i).click()

            print(
                "出發 8/15"
            )

            break



    page.wait_for_timeout(1000)



    # =====================
    # 選回程日期 22
    # =====================


    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):


        if days.nth(i).inner_text()=="22":


            days.nth(i).click()

            print(
                "回程 8/22"
            )

            break



    page.wait_for_timeout(2000)



    # =====================
    # 出發地
    # =====================


    inputs = page.locator(
        "input"
    )


    inputs.nth(2).fill(
        "TPE"
    )


    page.wait_for_timeout(2000)



    # 點第一個 TPE 選項

    try:

        page.get_by_text(
            "TPE",
            exact=False
        ).last.click(
            timeout=5000
        )


        print(
            "TPE完成"
        )


    except Exception as e:


        print(
            "TPE失敗",
            e
        )



    # =====================
    # 目的地
    # =====================


    page.locator(
        "#arrivalPlaceDesktop"
    ).fill(
        "PQC"
    )


    page.wait_for_timeout(2000)



    try:

        page.get_by_text(
            "PQC",
            exact=False
        ).last.click(
            timeout=5000
        )


        print(
            "PQC完成"
        )


    except Exception as e:


        print(
            "PQC失敗",
            e
        )



    # =====================
    # 查詢航班
    # =====================


    page.get_by_text(
        "查詢航班",
        exact=True
    ).click()



    page.wait_for_timeout(
        10000
    )



    send(
        "越捷查詢完成"
    )



    browser.close()
