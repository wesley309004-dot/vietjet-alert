from playwright.sync_api import sync_playwright
import os
import requests


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(t):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": t[:4000]
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



    # 打開日期

    page.get_by_text(
        "出發日期",
        exact=True
    ).first.locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click()


    page.wait_for_timeout(
        3000
    )



    send(
        "✅ 日期已開啟，開始抓HTML"
    )



    # 抓可能是calendar的元素

    elements = page.locator(
        "div,button,svg"
    )


    result = "=== CALENDAR ELEMENT DEBUG ===\n\n"


    count = 0


    for i in range(elements.count()):

        try:

            html = elements.nth(i).evaluate(
                "(e)=>e.outerHTML"
            )


            text = elements.nth(i).inner_text(
                timeout=500
            )


            if (
                "2026" in html
                or "七月" in html
                or "八月" in html
                or "calendar" in html.lower()
                or "chevron" in html.lower()
                or "arrow" in html.lower()
            ):

                result += f"""

--- ELEMENT {i} ---

TEXT:
{text[:300]}

HTML:
{html[:1500]}

================

"""


                count += 1


                if len(result) > 3500:

                    send(result)

                    result = (
                        "=== CONTINUE ===\n\n"
                    )


        except:
            pass



    result += (
        f"\n找到元素數量:{count}"
    )


    send(result)



    browser.close()
