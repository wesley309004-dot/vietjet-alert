import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


FROM = "TPE"
TO = "DAD"


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



def real_click(page, locator):

    locator.scroll_into_view_if_needed()

    locator.evaluate(
        """
        e => {

            e.dispatchEvent(
                new MouseEvent(
                    'mouseover',
                    {
                        bubbles:true
                    }
                )
            );


            e.dispatchEvent(
                new MouseEvent(
                    'mousedown',
                    {
                        bubbles:true
                    }
                )
            );


            e.dispatchEvent(
                new MouseEvent(
                    'mouseup',
                    {
                        bubbles:true
                    }
                )
            );


            e.click();

        }
        """
    )



def check_inputs(page):

    result=[]

    inputs=page.locator(
        "input"
    )


    for i in range(inputs.count()):

        try:

            value=inputs.nth(i).input_value()


            result.append(
                f"{i}: {value}"
            )

        except:

            pass


    send(
        "目前INPUT:\n"
        +
        "\n".join(result)
    )



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



    option = page.locator(
        "div"
    ).filter(
        has_text="臺北"
    ).filter(
        has_text="TPE"
    ).filter(
        has_text="桃園國際機場"
    ).first



    send(
        "TPE HTML:\n"
        +
        option.evaluate(
            "(e)=>e.outerHTML"
        )[:1000]
    )


    real_click(
        page,
        option
    )


    page.wait_for_timeout(5000)


    check_inputs(page)



def select_dad(page):

    log("🛬 選DAD")


    page.get_by_text(
        "目的地",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(8000)



    option = page.get_by_text(
        "DAD",
        exact=True
    ).last



    send(
        "DAD HTML:\n"
        +
        option.evaluate(
            "(e)=>e.outerHTML"
        )
    )



    real_click(
        page,
        option
    )


    page.wait_for_timeout(5000)


    check_inputs(page)



def main():


    send(
        "🚀 React Select Debug開始"
    )



    with sync_playwright() as p:


        browser=p.chromium.launch(
            headless=True
        )


        page=browser.new_page(
            locale="zh-TW"
        )


        try:

            open_page(page)

            cookie(page)

            select_tpe(page)

            select_dad(page)


            send(
                "🎉完成"
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
