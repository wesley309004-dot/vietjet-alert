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
        print(e)



def log(msg):

    print(
        datetime.datetime.now(),
        msg
    )



def wait(page, sec):

    page.wait_for_timeout(sec*1000)



def click_search(page):

    log("點查詢航班")


    button = page.locator(
        "button.MuiButton-contained"
    ).filter(
        has_text="查詢航班"
    ).first


    button.click(
        force=True,
        timeout=15000
    )



def select_airport(page, code, arrival=False):


    if arrival:

        box = page.locator(
            "#arrivalPlaceDesktop"
        )

    else:

        # 沒有id，用label找下面input

        box = page.locator(
            "label",
            has_text="出發地點"
        ).locator(
            ".."
        ).locator(
            "input"
        )



    log(
        f"輸入 {code}"
    )


    box.click(
        force=True
    )


    box.fill(
        code
    )


    wait(
        page,
        3
    )


    # 點選項

    option = page.get_by_text(
        code,
        exact=False
    ).last


    option.click(
        force=True,
        timeout=15000
    )


    log(
        f"{code}完成"
    )



def select_date(page):


    log(
        "日期"
    )


    page.get_by_text(
        "出發日期",
        exact=True
    ).click(
        force=True
    )


    wait(
        page,
        2
    )


    # 測試固定八月

    while True:

        month = page.locator(
            ".rdrMonthAndYearPickers"
        ).first.inner_text()


        log(month)


        if "八月" in month:

            break


        page.locator(
            "button.rdrNextButton"
        ).click(
            force=True
        )

        wait(
            page,
            1
        )



    days = page.locator(
        ".rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="15":

            days.nth(i).click(
                force=True
            )

            break



    wait(
        page,
        2
    )


    days = page.locator(
        ".rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="22":

            days.nth(i).click(
                force=True
            )

            break


    log(
        "日期完成"
    )



def main():


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        try:


            log(
                "開啟網站"
            )


            page.goto(
                "https://www.vietjetair.com/zh-TW",
                timeout=60000
            )


            wait(
                page,
                8000
            )


            # cookie

            try:

                page.get_by_text(
                    "接受",
                    exact=True
                ).click(
                    timeout=3000
                )

            except:

                pass



            select_date(
                page
            )


            select_airport(
                page,
                "TPE",
                False
            )


            select_airport(
                page,
                "CTS",
                True
            )


            click_search(
                page
            )


            wait(
                page,
                10000
            )


            log(
                page.url
            )


            if "select-flight" in page.url:


                send(
                    "✅ CTS成功\n"
                    + page.url
                )


            else:


                send(
                    "⚠️ 未進入航班頁\n"
                    + page.url
                )



        except Exception as e:


            err = traceback.format_exc()

            print(err)


            send(
                "❌錯誤\n\n"
                + str(e)
                + "\n\n"
                + err[-2000:]
            )



        finally:

            browser.close()



if __name__=="__main__":

    main()
