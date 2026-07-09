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



def main():

    send(
        "🚀 日期DOM Debug開始"
    )


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        try:


            page.goto(
                "https://www.vietjetair.com/zh-TW",
                timeout=60000
            )


            page.wait_for_timeout(
                10000
            )


            try:

                page.get_by_text(
                    "接受",
                    exact=True
                ).click(
                    timeout=5000
                )

            except:

                pass



            result = "=== INPUT DEBUG ===\n\n"


            inputs = page.locator(
                "input"
            )


            result += (
                "INPUT數量:"
                +
                str(inputs.count())
                +
                "\n\n"
            )


            for i in range(inputs.count()):


                try:


                    html = inputs.nth(i).evaluate(
                        "(e)=>e.outerHTML"
                    )


                    parent = inputs.nth(i).evaluate(
                        "(e)=>e.parentElement.outerHTML"
                    )


                    value = inputs.nth(i).input_value()



                    result += f"""
--- INPUT {i} ---

VALUE:
{value}

HTML:
{html[:800]}

PARENT:
{parent[:1500]}

"""


                except Exception as e:


                    result += f"""
INPUT {i} ERROR:
{e}

"""



            send(result)



            for text in [
                "出發日期",
                "返程日期"
            ]:


                try:


                    loc = page.get_by_text(
                        text,
                        exact=True
                    ).first



                    html = loc.evaluate(
                        "(e)=>e.outerHTML"
                    )


                    parent = loc.evaluate(
                        "(e)=>e.parentElement.outerHTML"
                    )


                    send(
f"""
=== {text} ===

HTML:
{html[:1000]}


PARENT:
{parent[:3000]}

"""
                    )


                except Exception as e:


                    send(
                        f"{text} ERROR\n{e}"
                    )



        except Exception as e:


            send(
                "❌錯誤\n"
                +
                str(e)
            )



        finally:


            browser.close()



if __name__ == "__main__":

    main()
