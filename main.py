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



    page.get_by_text(
        "出發日期",
        exact=True
    ).first.locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click()



    page.wait_for_timeout(
        3000
    )


    buttons=page.locator(
        "button"
    )


    result="=== BUTTON DEBUG ===\n\n"


    for i in range(buttons.count()):

        try:

            txt=buttons.nth(i).inner_text()

            aria=buttons.nth(i).get_attribute(
                "aria-label"
            )

            title=buttons.nth(i).get_attribute(
                "title"
            )


            if txt or aria or title:

                result+=f"""
BUTTON {i}

TEXT:
{txt}

ARIA:
{aria}

TITLE:
{title}

----------------

"""

        except:
            pass



    send(result)


    browser.close()

- name: Upload debug
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: debug
    path: debug/
