import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


GO_DATE = "2026-10-20"
RETURN_DATE = "2026-10-24"


api_logs = []



def send(text):

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text[:4000]
        },
        timeout=20
    )



def log(text):

    print(text)
    send(text)



def setup_response(page):


    def handler(res):

        url = res.url.lower()


        keys = [
            "flight",
            "fare",
            "price",
            "availability",
            "journey",
            "segment",
            "search",
            "booking"
        ]


        if any(
            k in url
            for k in keys
        ):


            try:

                body = res.text()

            except:

                body=""


            api_logs.append(
                {
                    "status":res.status,
                    "url":res.url,
                    "body":body[:1000]
                }
            )


    page.on(
        "response",
        handler
    )



def real_click(page, locator):

    locator.scroll_into_view_if_needed()

    locator.evaluate(
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



def open_page(page):

    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000
    )

    page.wait_for_timeout(10000)



def cookie(page):

    try:

        page.get_by_text(
            "接受",
            exact=True
        ).click(
            timeout=5000
        )

    except:

        pass



def select_tpe(page):

    page.get_by_text(
        "出發地點",
        exact=True
    ).click(
        force=True
    )

    page.wait_for_timeout(5000)


    page.get_by_text(
        "台灣 (6)",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)


    code = page.locator(
        "div.jss829"
    ).filter(
        has_text="TPE"
    ).first


    box = code.locator(
        "xpath=ancestor::div[contains(@class,'MuiBox-root')][1]"
    )


    real_click(
        page,
        box
    )


    page.wait_for_timeout(5000)



def select_dad(page):

    page.get_by_text(
        "目的地",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(8000)


    dad = page.get_by_text(
        "DAD",
        exact=True
    ).last


    real_click(
        page,
        dad
    )


    page.wait_for_timeout(5000)



def choose_day(page,date):

    day=date.split("-")[2]


    target=page.get_by_text(
        str(int(day)),
        exact=True
    ).last


    real_click(
        page,
        target
    )


    page.wait_for_timeout(3000)



def dates(page):

    page.get_by_text(
        "出發日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)


    choose_day(
        page,
        GO_DATE
    )


    page.get_by_text(
        "返程日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(5000)


    choose_day(
        page,
        RETURN_DATE
    )



def search(page):

    btn = page.get_by_text(
        "查詢航班",
        exact=True
    ).last


    btn.evaluate(
        "(e)=>e.click()"
    )


    page.wait_for_timeout(
        40000
    )


    log(
        "URL:\n"
        +
        page.url
    )



def analyze_result(page):


    send(
        "API數量:"
        +
        str(len(api_logs))
    )


    for x in api_logs[:10]:

        send(
            f"""
STATUS:
{x['status']}

URL:
{x['url'][:400]}

BODY:
{x['body'][:800]}
"""
        )



    try:

        text = page.locator(
            "body"
        ).inner_text()


        send(
            "結果頁文字:\n"
            +
            text[:2000]
        )

    except:

        pass



def main():

    send(
        "🚀 select-flight抓取開始"
    )


    with sync_playwright() as p:


        browser=p.chromium.launch(
            headless=True
        )


        page=browser.new_page(
            locale="zh-TW"
        )


        try:

            setup_response(page)

            open_page(page)

            cookie(page)

            select_tpe(page)

            select_dad(page)

            dates(page)

            search(page)

            analyze_result(page)


            send(
                "🎉完成"
            )


        except Exception as e:

            send(
                "❌錯誤\n"
                +
                str(e)
            )


        finally:

            browser.close()



if __name__=="__main__":

    main()
