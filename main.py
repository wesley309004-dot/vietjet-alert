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


    browser = p.chromium.launch(headless=True)


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
        ).click(timeout=3000)

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



    while True:

        month = page.locator(
            ".rdrMonthAndYearPickers"
        ).first.inner_text()


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
    # 出發地
    # =====================


    text_inputs = page.locator(
        "input[type='text']"
    )


    depart = text_inputs.nth(0)


    depart.fill(
        "TPE"
    )


    page.wait_for_timeout(3000)



    # 點桃園選項

    try:

        option = page.locator(
            "text=桃園國際機場"
        ).last


        option.click(
            timeout=5000
        )


        send(
            "TPE選取成功"
        )


    except Exception as e:


        send(
            "TPE選取失敗\n"+str(e)
        )



    page.wait_for_timeout(2000)



    # =====================
    # 目的地
    # =====================


    arrival = page.locator(
        "#arrivalPlaceDesktop"
    )


    arrival.fill(
        "PQC"
    )


    page.wait_for_timeout(3000)



    try:

        option = page.locator(
            "text=富國"
        ).last


        option.click(
            timeout=5000
        )


        send(
            "PQC選取成功"
        )


    except Exception as e:


        send(
            "PQC選取失敗\n"+str(e)
        )



    page.wait_for_timeout(2000)



    # 查詢

    try:

        page.get_by_text(
            "查詢航班",
            exact=True
        ).click(
            timeout=5000
        )


        send(
            "查詢已送出"
        )


    except Exception as e:


        send(
            "查詢失敗\n"+str(e)
        )



    page.wait_for_timeout(10000)


    browser.close()
