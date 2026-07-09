import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]



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

    inputs = page.locator(
        "input"
    )


    result=[]


    for i in range(inputs.count()):

        try:

            result.append(
                f"{i}: {inputs.nth(i).input_value()}"
            )

        except:

            pass


    send(
        "INPUT:\n"
        +
        "\n".join(result)
    )



def main():


    send(
        "🚀 TPE精準父層測試"
    )



    with sync_playwright() as p:


        browser=p.chromium.launch(
            headless=True
        )


        page=browser.new_page(
            locale="zh-TW"
        )



        try:


            page.goto(
                "https://www.vietjetair.com/zh-TW",
                timeout=60000
            )


            page.wait_for_timeout(10000)



            try:

                page.get_by_text(
                    "接受",
                    exact=True
                ).click(
                    timeout=5000
                )

            except:

                pass



            # 開出發地

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



            # 找 TPE

            tpe_code = page.locator(
                "div.jss829"
            ).filter(
                has_text="TPE"
            ).first



            send(
                "TPE CODE HTML:\n"
                +
                tpe_code.evaluate(
                    "(e)=>e.outerHTML"
                )
            )



            # 往上找真正選項

            box = tpe_code.locator(
                "xpath=ancestor::div[contains(@class,'MuiBox-root')][1]"
            )



            send(
                "BOX HTML:\n"
                +
                box.evaluate(
                    "(e)=>e.outerHTML"
                )[:1500]
            )



            real_click(
                page,
                box
            )


            page.wait_for_timeout(5000)



            check_inputs(page)



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
