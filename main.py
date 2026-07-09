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



    try:
        page.get_by_text(
            "接受",
            exact=True
        ).click(
            timeout=3000
        )
    except:
        pass



    target=page.get_by_text(
        "出發日期",
        exact=True
    ).first



    for i in range(1,6):

        try:

            html=target.locator(
                "xpath=" + "/.."*i
            ).evaluate(
                "(e)=>e.outerHTML"
            )


            send(
f"""
===== 第{i}層 =====

{html[:2000]}
"""
            )


        except Exception as e:

            send(
                f"{i} ERROR {e}"
            )



    browser.close()
