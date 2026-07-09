import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    r = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    print("Telegram:", r.status_code, r.text)


try:

    print("=== 開始 ===")

    result = "=== Vietjet TPE DOM Debug ===\n\n"


    with sync_playwright() as p:


        browser = p.chromium.launch(
            headless=True
        )


        page = browser.new_page(
            locale="zh-TW",
            viewport={
                "width":1280,
                "height":900
            }
        )


        print("開啟網站")


        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        page.wait_for_timeout(8000)



        # Cookie

        try:

            page.locator("h5").filter(
                has_text="接受"
            ).click(
                timeout=5000
            )

            page.wait_for_timeout(2000)

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



        # 截圖

        page.screenshot(
            path="vietjet_debug.png",
            full_page=True
        )


        print("搜尋TPE")


        divs = page.locator(
            "div"
        ).filter(
            has_text="TPE"
        )


        count = divs.count()


        result += f"TPE div數量：{count}\n\n"


        print(
            "找到:",
            count
        )



        for i in range(count):

            try:

                txt = divs.nth(i).inner_text(
                    timeout=3000
                )


                html = divs.nth(i).evaluate(
                    "(e)=>e.outerHTML"
                )


                print(
                    "\n第",
                    i,
                    "個"
                )

                print(
                    repr(txt[:300])
                )


                result += (
                    "\n================\n"
                )

                result += (
                    f"第 {i} 個\n\n"
                )

                result += (
                    "TEXT:\n"
                    + txt[:500]
                    + "\n\n"
                )

                result += (
                    "HTML:\n"
                    + html[:500]
                    + "\n"
                )


            except Exception as e:

                result += (
                    f"\n第{i}個錯誤:"
                    + str(e)
                    + "\n"
                )



        body = page.locator(
            "body"
        ).inner_text()


        if "最近到達目的地" in body:

            result += "\n\n選單仍存在"

        else:

            result += "\n\n選單可能關閉"



        print(result)


        send(result)


        browser.close()



except Exception as e:


    error = (
        "程式錯誤:\n\n"
        + str(e)
    )

    print(error)

    send(error)
