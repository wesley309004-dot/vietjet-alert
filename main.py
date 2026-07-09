taipei = page.get_by_text(
    "TPE",
    exact=False
)

result += "TPE數量：" + str(taipei.count()) + "\n"

if taipei.count() > 0:
    taipei.last.click(force=True)
    page.wait_for_timeout(3000)
    result += "成功點擊TPE\n"
else:
    result += "找不到TPE\n"
