from playwright.sync_api import sync_playwright
import os
import requests


TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


def send(t):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": t[:4000]
        },
        timeout=20
    )


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )


    page = browser.new_page(
        locale="zh-TW"
    )


    try:

        send("🚀 Calendar DOM完整測試開始")


        page.goto(
            "https://www.vietjetair.com/zh-TW",
            timeout=60000
        )


        page.wait_for_timeout(
            8000
        )


        try:

            page.get_by_text(
                "接受",
                exact=True
            ).click(
                timeout=3000
            )

        except:

            pass



        # 開啟日期

        page.get_by_text(
            "出發日期",
            exact=True
        ).first.locator(
            "xpath=ancestor::div[@role='button'][1]"
        ).click()



        page.wait_for_timeout(
            3000
        )


        send(
            "✅ 日期面板已開啟"
        )



        # 找月份

        month = page.get_by_text(
            "七月 2026",
            exact=True
        ).first



        if month.count() == 0:

            send(
                "❌ 找不到 七月2026"
            )

        else:


            send(
                "✅ 找到七月2026\n\n"
                +
                month.evaluate(
                    "(e)=>e.outerHTML"
                )[:2000]
            )



            for i in range(1,8):

                try:

                    html = month.locator(
                        "xpath=" + "/.." * i
                    ).evaluate(
                        "(e)=>e.outerHTML"
                    )


                    send(
f"""
===== 第{i}層 =====

{html[:3500]}

"""
                    )


                except Exception as e:

                    send(
                        f"第{i}層錯誤\n{e}"
                    )



        send(
            "🎉 Calendar DOM測試完成"
        )


    except Exception as e:

        send(
            "❌錯誤\n"
            +
            str(e)
        )


    finally:

        browser.close()
