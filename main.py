from playwright.sync_api import sync_playwright
import os
import requests


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


    page.wait_for_timeout(3000)



    while True:

        month = page.locator(
            ".rdrMonthAndYearPickers"
        ).first.inner_text()


        print(month)


        if month == "八月 2026":

            break


        page.locator(
            "button.rdrNextButton"
        ).first.click()


        page.wait_for_timeout(500)



    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="15":

            days.nth(i).click()

            break



    page.wait_for_timeout(1000)



    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="22":

            days.nth(i).click()

            break



    page.wait_for_timeout(2000)



    # =====================
    # 出發地 TPE
    # =====================


    inputs = page.locator(
        "input[type='text']"
    )


    depart = inputs.filter(
        has_not=page.locator("[readonly]")
    ).first



    depart.fill(
        "TPE"
    )


    page.wait_for_timeout(3000)



    text = page.locator(
        "body"
    ).inner_text()



    send(
        "輸入TPE後畫面:\n\n"+text[:3000]
    )



    # 嘗試點選 TPE


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


        send(
            "TPE點擊失敗\n"+str(e)
        )



    page.wait_for_timeout(2000)



    # =====================
    # 目的地 PQC
    # =====================


    arrival = page.locator(
        "#arrivalPlaceDesktop"
    )


    arrival.fill(
        "PQC"
    )


    page.wait_for_timeout(3000)



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


        send(
            "PQC點擊失敗\n"+str(e)
        )



    page.wait_for_timeout(2000)



    # =====================
    # 查詢
    # =====================


    try:

        page.get_by_text(
            "查詢航班",
            exact=True
        ).click(
            timeout=5000
        )


        send(
            "已送出查詢"
        )


    except Exception as e:


        send(
            "查詢失敗\n"+str(e)
        )



    page.wait_for_timeout(10000)


    browser.close()
