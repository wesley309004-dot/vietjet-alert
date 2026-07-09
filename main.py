import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


FROM = "TPE"
TO = "DAD"

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



def real_click(page, locator):

    locator.scroll_into_view_if_needed()

    locator.evaluate(
        """
        e => {

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



def check_inputs(page):

    inputs = page.locator("input")

    result=[]

    for i in range(inputs.count()):

        try:

            result.append(
                f"{i}: {inputs.nth(i).input_value()}"
            )

        except:

            pass


    send(
        "目前INPUT:\n"
        +
        "\n".join(result)
    )



def setup_api(page):


    def response(res):

        url=res.url.lower()


        if any(
            x in url
            for x in [
                "flight",
                "search",
                "booking",
                "availability",
                "api"
            ]
        ):


            if (
                "google" not in url
                and
                "analytics" not in url
            ):


                try:

                    body=res.text()

                except:

                    body=""


                api_logs.append(
                    {
                        "status":res.status,
                        "url":res.url,
                        "body":body[:500]
                    }
                )


    page.on(
        "response",
        response
    )



def open_page(page):

    log("🌐 開啟 Vietjet")


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

        log("🍪 Cookie完成")

    except:

        pass



def select_tpe(page):

    log("🇹🇼 選TPE")


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



    tpe_code = page.locator(
        "div.jss829"
    ).filter(
        has_text="TPE"
    ).first



    box = tpe_code.locator(
        "xpath=ancestor::div[contains(@class,'MuiBox-root')][1]"
    )


    real_click(
        page,
        box
    )


    page.wait_for_timeout(5000)


    log("✅ TPE完成")



def select_dad(page):

    log("🛬 選DAD")


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


    log("✅ DAD完成")



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



def select_date(page):

    log("📅 日期")


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


    log("✅ 日期完成")



def search(page):

    log("🔍 查詢")


    check_inputs(page)



    btn=page.get_by_text(
        "查詢航班",
        exact=True
    ).last


    btn.evaluate(
        "(e)=>e.click()"
    )


    page.wait_for_timeout(
        30000
    )



    send(
        "最後URL:\n"
        +
        page.url
    )


    send(
        "API數量:"
        +
        str(len(api_logs))
    )



    for x in api_logs[:5]:

        send(
            f"""
STATUS:
{x['status']}

URL:
{x['url'][:300]}

BODY:
{x['body'][:500]}
"""
        )



def main():

    send(
        "🚀 Vietjet完整版測試"
    )


    with sync_playwright() as p:


        browser=p.chromium.launch(
            headless=True
        )


        page=browser.new_page(
            locale="zh-TW"
        )


        try:

            setup_api(page)

            open_page(page)

            cookie(page)

            select_tpe(page)

            select_dad(page)

            select_date(page)

            search(page)


            send(
                "🎉流程完成"
            )


        except Exception as e:

            send(
                "❌錯誤\n"
                +str(e)
            )


        finally:

            browser.close()



if __name__=="__main__":

    main()
