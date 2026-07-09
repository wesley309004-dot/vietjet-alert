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

    print("Telegram 回應:")
    print(r.status_code)
    print(r.text)


try:

    print("=== 程式開始 ===")


    with sync_playwright() as p:

        print("啟動瀏覽器")

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            locale="zh-TW"
        )


        print("開啟 Vietjet")

        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        print("等待頁面載入")

        page.wait_for_timeout(8000)


        result = "=== TPE選項定位 ===\n\n"


        # 接受 Cookie
        try:

            print("嘗試接受 Cookie")

            page.locator("h5").filter(
                has_text="接受"
            ).click(
                timeout=5000
            )

            page.wait_for_timeout(2000)

            print("Cookie 完成")

        except:

            print("沒有 Cookie 視窗")


        # 點擊出發地點

        print("點擊出發地點")

        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(3000)


        print("搜尋 TPE")


        divs = page.locator("div").filter(
            has_text="TPE"
        )


        count = divs.count()


        print(
            "找到 TPE div:",
            count
        )


        result += "包含TPE div數量："
        result += str(count)
        result += "\n\n"


        clicked = False


        for i in range(min(count, 10)):

            try:

                txt = divs.nth(i).inner_text()

                print(
                    "第",
                    i,
                    "個:",
                    txt[:100]
                )


                if "桃園" in txt:


                    result += "找到選項:\n"
                    result += txt[:300]
                    result += "\n\n"


                    divs.nth(i).click(
                        force=True,
                        timeout=5000
                    )


                    page.wait_for_timeout(3000)


                    result += "已點擊此區塊\n"

                    clicked = True

                    break


            except Exception as e:

                print(
                    "定位錯誤:",
                    e
                )


        if not clicked:

            result += "沒有成功點擊桃園選項\n"



        body = page.locator(
            "body"
        ).inner_text()


        if "最近到達目的地" in body:

            result += "\n選單仍存在"

        else:

            result += "\n選單已關閉"



        print("=====結果=====")
        print(result)


        send(result)


        browser.close()



except Exception as e:


    error = (
        "Vietjet監控錯誤:\n\n"
        + str(e)
    )


    print(error)

    send(error)
