import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


GO_DATE = "2026-10-20"
RETURN_DATE = "2026-10-24"



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



def choose_date(page, target):

    year, month, day = target.split("-")

    month = int(month)
    day = int(day)


    log(
        f"📅目標日期 {year}/{month}/{day}"
    )


    # 找日期視窗文字

    page.wait_for_timeout(3000)



    # 印目前calendar文字

    try:

        calendar = page.locator(
            "body"
        ).inner_text()


        send(
            "目前日期區塊:\n"
            +
            calendar[:1000]
        )

    except:

        pass



    # 找下一月按鈕

    for i in range(6):


        text = page.locator(
            "body"
        ).inner_text()


        # 已經到目標月份

        if (
            f"{month}月" in text
            or
            f"{month} 月" in text
        ):

            break



        buttons = page.locator(
            "button"
        )


        clicked=False


        for j in range(buttons.count()):

            try:

                aria = buttons.nth(j).get_attribute(
                    "aria-label"
                )


                title = buttons.nth(j).get_attribute(
                    "title"
                )


                if (
                    aria
                    and
                    (
                        "next" in aria.lower()
                        or
                        "下一" in aria
                    )
                ):

                    real_click(
                        page,
                        buttons.nth(j)
                    )

                    clicked=True
                    break


                if (
                    title
                    and
                    (
                        "next" in title.lower()
                        or
                        "下一" in title
                    )
                ):

                    real_click(
                        page,
                        buttons.nth(j)
                    )

                    clicked=True
                    break


            except:

                pass



        if not clicked:

            send(
                "⚠️找不到下一月按鈕"
            )

            break


        page.wait_for_timeout(2000)



    # 點日期

    day_locator = page.locator(
        "button"
    ).filter(
        has_text=str(day)
    ).last


    real_click(
        page,
        day_locator
    )


    page.wait_for_timeout(5000)



def select_dates(page):


    log(
        "📅開始選日期"
    )


    page.get_by_text(
        "出發日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(3000)



    choose_date(
        page,
        GO_DATE
    )



    page.get_by_text(
        "返程日期",
        exact=True
    ).click(
        force=True
    )


    page.wait_for_timeout(3000)



    choose_date(
        page,
        RETURN_DATE
    )


    log(
        "✅日期完成"
    )



def main():


    send(
        "🚀日期測試版"
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


            page.wait_for_timeout(8000)


            select_dates(page)


            send(
                page.locator(
                    "body"
                ).inner_text()[:2000]
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
