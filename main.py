import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(text):

    print("準備發送 Telegram")

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


    # Telegram 一則最多約4096字
    chunks = [
        text[i:i+3500]
        for i in range(0, len(text), 3500)
    ]


    for c in chunks:

        r = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": c
            },
            timeout=20
        )

        print(
            "Telegram狀態:",
            r.status_code,
            r.text[:200]
        )



try:

    print("=== 程式開始 ===")


    result = "=== Vietjet TPE Debug ===\n"


    with sync_playwright() as p:


        print("啟動瀏覽器")


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW"
        )


        print("開啟網站")


        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        print("網站完成")


        page.wait_for_timeout(8000)



        try:

            page.locator("h5").filter(
                has_text="接受"
            ).click(
                timeout=5000
            )

            print("Cookie關閉")

        except:

            print("沒有Cookie")



        print("點擊出發地")


        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(3000)


        print("搜尋TPE")


        divs = page.locator(
            "div"
        ).filter(
            has_text="TPE"
        )


        count = divs.count()


        print(
            "TPE數量:",
            count
        )


        result += f"\nTPE數量:{count}\n"



        for i in range(count):

            try:

                txt = divs.nth(i).inner_text()

                html = divs.nth(i).evaluate(
                    "(e)=>e.outerHTML"
                )


                print(
                    "第",
                    i,
                    "個:",
                    txt[:100]
                )


                result += (
                    "\n---第"
                    + str(i)
                    + "個---\n"
                )

                result += (
                    txt[:300]
                    + "\n"
                )

                result += (
                    html[:300]
                    + "\n"
                )


            except Exception as e:

                print(
                    "抓取錯誤",
                    i,
                    e
                )



        print("準備送Telegram")


        send(result)


        browser.close()



except Exception as e:


    print(
        "錯誤:",
        e
    )


    send(
        "Vietjet錯誤:\n"
        + str(e)
    )
