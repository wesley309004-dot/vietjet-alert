from playwright.sync_api import sync_playwright, TimeoutError
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
        print("Telegram error", e)


def log(msg):
    print(
        datetime.datetime.now().strftime("%H:%M:%S"),
        msg,
        flush=True
    )


def wait(page, sec):
    page.wait_for_timeout(sec * 1000)



def open_site(page):

    log("START 開啟越捷")

    page.goto(
        "https://www.vietjetair.com/zh-TW",
        timeout=60000,
        wait_until="domcontentloaded"
    )

    wait(page,8)

    log("首頁完成")


    try:
        page.get_by_text(
            "接受",
            exact=True
        ).click(
            timeout=3000
        )

        log("Cookie完成")

    except:
        log("無Cookie")



def choose_date(page):

    log("START 日期")

    page.get_by_text(
        "出發日期",
        exact=True
    ).locator(
        "xpath=ancestor::div[@role='button'][1]"
    ).click(
        timeout=10000
    )


    wait(page,3)


    found=False


    for i in range(12):

        try:

            month = page.locator(
                ".rdrMonthAndYearPickers"
            ).first.inner_text(
                timeout=3000
            )

            log(
                "目前月份 "+month
            )


            if "八月 2026" in month:

                found=True
                break


            page.locator(
                "button.rdrNextButton"
            ).first.click(
                force=True,
                timeout=5000
            )

            wait(page,1)


        except Exception as e:

            log(
                "月份錯誤 "+str(e)
            )



    if not found:

        raise Exception(
            "找不到八月2026"
        )



    days = page.locator(
        ".rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="15":

            days.nth(i).click(
                force=True
            )

            log(
                "出發15完成"
            )

            break


    wait(page,2)


    days = page.locator(
        ".rdrDay:not(.rdrDayPassive)"
    )


    for i in range(days.count()):

        if days.nth(i).inner_text()=="22":

            days.nth(i).click(
                force=True
            )

            log(
                "回程22完成"
            )

            break


    wait(page,2)

    log("DONE 日期")



def airport(page, code):


    log(
        "START 機場 "+code
    )


    # 找所有文字input
    inputs = page.locator(
        "input[type='text']"
    )


    count = inputs.count()

    log(
        "input數量 "+str(count)
    )


    target=None


    for i in range(count):

        value=inputs.nth(i).input_value()

        log(
            f"input {i}: {value}"
        )


        if value=="" or "(" in value:

            target=inputs.nth(i)


    if target is None:

        raise Exception(
            "找不到機場輸入框"
        )



    target.click(
        force=True
    )


    target.fill(
        code
    )


    wait(page,3)



    # 不用last
    options = page.get_by_text(
        code,
        exact=False
    )


    total=options.count()


    log(
        "找到選項數 "+str(total)
    )


    for i in range(total):

        txt=options.nth(i).inner_text()

        log(
            "選項:"+txt
        )


        if code in txt:

            options.nth(i).click(
                force=True,
                timeout=5000
            )

            log(
                code+"完成"
            )

            return



    raise Exception(
        code+"找不到"
    )



def search(page):


    log(
        "START 查詢"
    )


    btn=page.locator(
        "button"
    ).filter(
        has_text="查詢航班"
    ).first


    btn.click(
        force=True,
        timeout=10000
    )


    wait(page,15)


    log(
        "網址:"+page.url
    )


    if "select-flight" in page.url:

        log(
            "成功進入航班頁"
        )

        return True


    return False




def main():


    with sync_playwright() as p:


        browser=p.chromium.launch(
            headless=True
        )


        page=browser.new_page(
            locale="zh-TW"
        )


        try:


            open_site(page)


            choose_date(page)


            airport(
                page,
                "TPE"
            )


            wait(page,3)


            airport(
                page,
                "CTS"
            )


            wait(page,3)


            result=search(page)


            if result:

                body=page.locator(
                    "body"
                ).inner_text(
                    timeout=10000
                )


                send(
                    "✅ CTS成功\n\n"
                    +page.url
                    +"\n\n"
                    +body[:2500]
                )


            else:

                send(
                    "⚠️ 未進入航班頁\n"
                    +page.url
                )



        except Exception as e:


            err=traceback.format_exc()

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
