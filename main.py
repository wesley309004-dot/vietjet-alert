import os
import requests
from datetime import date, timedelta

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

PRICE_LIMIT_TOTAL = 10000
PRICE_LIMIT_ONEWAY = 2000


def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


def generate_dates():

    periods = []

    # 1月15日～1月底
    periods.append(
        (
            date(2027,1,15),
            date(2027,1,31),
            date(2027,2,1)
        )
    )

    # 2月11日～2月19日
    periods.append(
        (
            date(2027,2,11),
            date(2027,2,19),
            date(2027,2,28)
        )
    )

    # 2月22日～3月底
    periods.append(
        (
            date(2027,2,22),
            date(2027,3,31),
            date(2027,3,31)
        )
    )


    result = []

    for start,end,max_return in periods:

        current = start

        while current <= end:

            for days in [6,7]:

                back = current + timedelta(days=days)

                if back <= max_return:
                    result.append(
                        (
                            current.isoformat(),
                            back.isoformat()
                        )
                    )

            current += timedelta(days=1)

    return result



dates = generate_dates()


message = (
    "✈️ Vietjet札幌監控啟動\n\n"
    f"目前監控日期組合：{len(dates)} 組\n\n"
    "範例：\n"
)

for d in dates[:5]:
    message += f"{d[0]} → {d[1]}\n"


send_message(message)
