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



    # 接受cookie

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


    page.wait_for_timeout(3000)



    # 切到八月2026

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


        page.wait_for_timeout(800)



    print(
        "月份完成"
    )



    # 選日期 8/15

    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text() == "15":

            days.nth(i).click()

            print(
                "選出發 8/15"
            )

            break



    page.wait_for_timeout(1000)



    # 選日期 8/22

    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text() == "22":

            days.nth(i).click()

            print(
                "選回程 8/22"
            )

            break



    page.wait_for_timeout(3000)



    # ==========================
    # DEBUG INPUT
    # ==========================


    inputs = page.locator(
        "input"
    )


    result = "=== INPUT DEBUG ===\n\n"


    result += f"INPUT數量:{inputs.count()}\n\n"



    for i in range(inputs.count()):

        try:

            html = inputs.nth(i).evaluate(
                "(e)=>e.outerHTML"
            )


            value = inputs.nth(i).input_value()


            result += f"""
INPUT {i}

VALUE:
{value}

HTML:
{html}

----------------

"""


        except Exception as e:

            result += f"""
INPUT {i}

ERROR:
{e}

----------------

"""



    send(result)



    browser.close()
