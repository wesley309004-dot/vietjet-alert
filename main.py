import os
import requests
from playwright.sync_api import sync_playwright


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(text):

    r = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=20
    )

    print(r.text)



try:

    result = "=== TPE精準點擊V2 ===\n\n"


    with sync_playwright() as p:


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


        page.wait_for_timeout(8000)



        try:

            page.locator("h5").filter(
                has_text="接受"
            ).click(
                timeout=5000
            )

            page.wait_for_timeout(2000)

        except:

            pass



        page.get_by_text(
            "出發地點",
            exact=True
        ).click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(3000)



        # 找TPE

        tpe = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).first



        result += "找到TPE\n\n"



        # 找真正選項盒

        option = tpe.locator(
            "xpath=../../"
        )


        # 如果上面失敗，改用祖先搜尋

        option = tpe.locator(
            "xpath=ancestor::div[contains(@class,'MuiBox-root')][1]"
        )



        result += (
            "點擊元素文字:\n"
            + option.inner_text()
            + "\n\n"
        )


        result += (
            "HTML:\n"
            + option.evaluate(
                "(e)=>e.outerHTML"
            )[:500]
            + "\n\n"
        )



        option.click(
            force=True,
            timeout=5000
        )


        page.wait_for_timeout(3000)



        result += "已點擊\n"



        # 檢查

        remain = page.locator(
            "div.jss829"
        ).filter(
            has_text="TPE"
        ).count()



        result += (
            "剩餘TPE:"
            + str(remain)
            + "\n"
        )


        if remain == 0:

            result += "成功關閉"

        else:

            result += "選單仍存在"



        send(result)


        browser.close()



except Exception as e:

    send(
        "錯誤:\n"
        + str(e)
    )
