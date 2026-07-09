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



    date_text=page.get_by_text(
        "出發日期",
        exact=True
    ).first



    button=date_text.locator(
        "xpath=ancestor::div[@role='button'][1]"
    )


    send(
        "日期按鈕數量:"
        +
        str(button.count())
    )



    html=button.evaluate(
        "(e)=>e.outerHTML"
    )


    send(
        "日期按鈕HTML:\n"
        +
        html[:2000]
    )



    button.evaluate(
        """
        e=>{
            e.dispatchEvent(
                new MouseEvent(
                    'mouseover',
                    {bubbles:true}
                )
            );
            e.dispatchEvent(
                new MouseEvent(
                    'mousedown',
                    {bubbles:true}
                )
            );
            e.dispatchEvent(
                new MouseEvent(
                    'mouseup',
                    {bubbles:true}
                )
            );
            e.click();
        }
        """
    )


    page.wait_for_timeout(
        5000
    )


    body=page.locator(
        "body"
    ).inner_text()


    send(
        "點擊後:\n"
        +
        body[:3000]
    )


    browser.close()
