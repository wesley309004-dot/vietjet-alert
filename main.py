# =====================
# 查詢航班
# =====================

try:

    buttons = page.get_by_role(
        "button",
        name="查詢航班"
    )

    print(
        "查詢按鈕數量:",
        buttons.count()
    )


    buttons.first.click(
        timeout=10000
    )


    print(
        "查詢航班點擊成功"
    )


except Exception as e:

    print(
        "查詢失敗",
        e
    )


page.wait_for_timeout(
    15000
)


send(
    "越捷查詢完成"
)
