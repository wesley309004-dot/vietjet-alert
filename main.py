from playwright.sync_api import sync_playwright
import os
import requests
import traceback
import datetime


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(msg):

    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": msg[:4000]
            },
            timeout=20
        )

    except Exception as e:
        print("Telegram error:", e)



def debug(msg):

    print(
        datetime.datetime.now(),
        msg
    )



def wait(page, sec=1):

    page.wait_for_timeout(
        sec * 1000
    )



def open_vietjet(page):

    debug("開啟越捷")

    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000
    )

    wait(page,8)


    try:

        page.get_by_text(
            "接受",
            exact=True
        ).click(
            timeout=3000
        )

        debug("Cookie完成")


    except:

        debug("沒有Cookie")



def select_date(page):

    debug("日期選擇")


    page.get_by_text(
        "出發日期",
        exact=True
    ).first.locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click(
        force=True
    )


    wait(page,2)


    while True:

        month = page.locator(
            ".rdrMonthAndYearPickers"
        ).first.inner_text()


        debug(
            "月份:"+month
        )


        if "八月" in month and "2026" in month:
            break


        page.locator(
            "button.rdrNextButton"
        ).first.click(
            force=True
        )

        wait(page,1)



    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="15":

            days.nth(i).click(
                force=True
            )

            debug("出發15完成")
            break



    wait(page,2)



    days = page.locator(
        ".rdrMonth button.rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="22":

            days.nth(i).click(
                force=True
            )

            debug("回程22完成")
            break



    wait(page,2)




def select_departure(page, code):


    debug(
        "選出發地 "+code
    )


    label = page.get_by_text(
        "出發地點",
        exact=True
    )


    input_box = label.locator(
        "xpath=following::input[1]"
    )


    input_box.click(
        force=True
    )


    input_box.fill(
        code
    )


    wait(page,3)


    page.get_by_text(
        code,
        exact=False
    ).last.click(
        force=True,
        timeout=10000
    )


    debug(
        "出發地完成"
    )




def select_arrival(page, code):


    debug(
        "選目的地 "+code
    )


    input_box = page.locator(
        "#arrivalPlaceDesktop"
    )


    input_box.click(
        force=True
    )


    input_box.fill(
        code
    )


    wait(page,3)


    page.get_by_text(
        code,
        exact=False
    ).last.click(
        force=True,
        timeout=10000
    )


    debug(
        "目的地完成"
    )





def search(page):


    debug(
        "查詢航班"
    )


    button = page.get_by_role(
        "button",
        name="查詢航班"
    ).first


    button.scroll_into_view_if_needed()


    wait(page,2)


    button.click(
        force=True,
        timeout=15000
    )


    wait(page,12)



    debug(
        "網址:"+page.url
    )


    if "select-flight" in page.url:

        return True

    return False





def main():


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        try:


            open_vietjet(page)


            select_date(page)


            select_departure(
                page,
                "TPE"
            )


            wait(page,2)


            select_arrival(
                page,
                "CTS"
            )


            wait(page,3)



            ok = search(page)



            if ok:


                body = page.locator(
                    "body"
                ).inner_text(
                    timeout=10000
                )


                send(
                    "✅ CTS成功\n\n"
                    +page.url
                    +"\n\n"
                    +body[:3000]
                )


            else:


                send(
                    "⚠️ 未進入航班頁\n"
                    +page.url
                )



        except Exception as e:


            err = traceback.format_exc()

            print(err)


            try:

                page.screenshot(
                    path="error.png",
                    full_page=True
                )

            except:

                pass



            send(
                "❌ 查詢異常\n\n"
                +str(e)
                +"\n\n"
                +err[-2000:]
            )



        finally:


            browser.close()





if __name__=="__main__":

    main()
