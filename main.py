import os
import requests
from playwright.sync_api import sync_playwright


FROM = "TPE"
TO = "DAD"

GO_DATE = "2026-10-20"
RETURN_DATE = "2026-10-24"


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



def mouse_click(page, locator):

    box = locator.bounding_box()

    if not box:
        return False


    page.mouse.click(
        box["x"] + box["width"]/2,
        box["y"] + box["height"]/2
    )

    return True



def open_page(page):

    log("🌐 開啟")

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

        log("🍪 Cookie")

    except:

        pass



def departure(page):

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


    tpe = page.locator(
        "div"
    ).filter(
        has_text="臺北"
    ).filter(
        has_text="TPE"
    ).filter(
        has_text="桃園國際機場"
    ).first


    mouse_click(
        page,
        tpe
    )


    page.wait_for_timeout(5000)

    log("✅ TPE")



def destination(page):

    page.get_by_text(
        "目的地",
        exact=True
    ).click(
        force=True
    )

    page.wait_for_timeout(8000)


    dad = page.get_by_text(
        TO,
        exact=True
    ).last


    mouse_click(
        page,
        dad
    )


    page.wait_for_timeout(5000)

    log("✅ DAD")



def choose_day(page,date):

    day = date.split("-")[2]


    target = page.get_by_text(
        str(int(day)),
        exact=True
    ).last


    mouse_click(
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


    log("✅ 日期")



# =====================
# 新增：Input檢查
# =====================

def inspect_inputs(page):

    log("🔎 檢查INPUT")


    inputs = page.locator(
        "input"
    )


    result = []



    for i in range(inputs.count()):

        try:

            value = inputs.nth(i).input_value()

        except:

            value = "ERROR"



        try:

            placeholder = inputs.nth(i).get_attribute(
                "placeholder"
            )

        except:

            placeholder = ""



        try:

            aria = inputs.nth(i).get_attribute(
                "aria-label"
            )

        except:

            aria = ""



        result.append(
            f"""
INPUT {i}

value:
{value}

placeholder:
{placeholder}

aria:
{aria}
"""
        )



    send(
        "INPUT結果:\n"
        +
        "\n".join(result[:20])
    )



def main():

    send(
        "🚀 Input State Debug"
    )


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        try:

            open_page(page)

            cookie(page)

            departure(page)

            destination(page)

            dates(page)


            inspect_inputs(page)



            send(
                "🎉完成"
            )


        except Exception as e:

            send(
                "❌錯誤\n"+str(e)
            )


        finally:

            browser.close()



if __name__=="__main__":

    main()
