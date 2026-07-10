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



    # 點出發日期

    page.get_by_text(
        "出發日期",
        exact=True
    ).first.locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click()


    page.wait_for_timeout(2000)



    # 到八月2026

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



    # 出發15

    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text() == "15":

            days.nth(i).click()

            print(
                "出發15完成"
            )

            break



    page.wait_for_timeout(1000)



    # 回程22

    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text() == "22":

            days.nth(i).click()

            print(
                "回程22完成"
            )

            break



    page.wait_for_timeout(1000)



    # 出發地

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
        "TPE PQC前"
    )



    # 目的地

    page.locator(
        "#arrivalPlaceDesktop"
    ).fill(
        "PQC"
    )


    page.wait_for_timeout(2000)



    page.get_by_text(
        "PQC",
        exact=False
    ).last.click(
        timeout=5000
    )


    print(
        "TPE PQC選取成功"
    )



    page.wait_for_timeout(2000)



    # 查詢

    try:

        page.get_by_role(
            "button",
            name="查詢航班"
        ).first.click(
            timeout=10000
        )


        print(
            "查詢按鈕成功"
        )


    except Exception as e:

        print(
            "查詢失敗",
            e
        )

        send(
            f"查詢失敗\n{e}"
        )

        browser.close()

        raise



    page.wait_for_timeout(
        15000
    )


    send(
        "越捷查詢完成"
    )


    browser.close()
