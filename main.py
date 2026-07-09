from playwright.sync_api import sync_playwright
import os
import requests


TOKEN=os.environ["TELEGRAM_TOKEN"]
CHAT_ID=os.environ["TELEGRAM_CHAT_ID"]


def send(t):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id":CHAT_ID,
            "text":t[:4000]
        }
    )


with sync_playwright() as p:

    browser=p.chromium.launch(
        headless=True
    )

    page=browser.new_page(
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
        ).click(timeout=3000)

    except:
        pass



    # 點日期

    page.get_by_text(
        "出發日期",
        exact=True
    ).first.locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click()


    page.wait_for_timeout(2000)



    # 找目前月份

    month = page.locator(
        ".rdrMonthAndYearPickers"
    ).first


    print(
        "目前:",
        month.inner_text()
    )



    # 點下一月直到 2026年8月

    while True:

        current=month.inner_text()

        print(
            "月份:",
            current
        )


        if current=="八月 2026":
            break


        page.locator(
            "button.rdrNextButton"
        ).first.click()


        page.wait_for_timeout(500)



    print("已到八月")



    # 選日期範例 8/15

    days=page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        txt=days.nth(i).inner_text()

        if txt=="15":

            days.nth(i).click()

            print(
                "選到15號"
            )

            break



    page.wait_for_timeout(1000)



    send(
        "日期選取完成"
    )


    browser.close()
