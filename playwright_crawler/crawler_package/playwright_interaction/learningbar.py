import asyncio
from playwright.async_api import async_playwright


async def main(playwright):
    json_container = {}
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(
        storage_state="/home/eric/文件/github/cookies_pack/learningbar_cookies")

    # Open new page
    page = await context.new_page()

    # Go to https://www.learningbar.tw/
    await page.goto("https://www.learningbar.tw/")

    # Click text=登入學Bar
    await page.frame(name="LBR_Banner").click("text=登入學Bar")

    # Click [placeholder="E-mail"]
    await page.frame(name="LBR_Body").click("[placeholder=\"E-mail\"]")

    # Fill [placeholder="E-mail"]
    await page.frame(name="LBR_Body").fill(
        "[placeholder=\"E-mail\"]", "ericcheng26@gmail.com")

    # Press Tab
    await page.frame(name="LBR_Body").press("[placeholder=\"E-mail\"]", "Tab")

    # Fill [placeholder="Password"]
    await page.frame(name="LBR_Body").fill(
        "[placeholder=\"Password\"]", "HACKER26")

    # Check [placeholder="Password tabindex="]
    await page.frame(name="LBR_Body").check(
        "[placeholder=\"Password tabindex=\"]")

    # Click input:has-text("登入")
    await page.frame(name="LBR_Body").click("input:has-text(\"登入\")")

    # Click text=分類瀏覽
    await page.frame(name="LBR_Body").click("text=分類瀏覽")
    # 每次先選擇不同類別，再做相同行爲
    # 行爲=抓取所有"出處xxxx"的element，然後將文字取出
    # 嘗試：取出文字後下一頁，並執行"行爲"，直到
    for x in range(44, 98):
        await page.frame(name="LBR_Body").select_option("select[name=\"s_Question_Subject\"]", f"SUB-0{x}")
        await page.frame(name="LBR_Body").click("text=送出")
    # 找出含有"出處: 民國xxxxx" 的element並用list裝起來
        lst_ = page.frame(name="LBR_Body").query_selector_all(
            'text=/出處: 民國 \d{2,3} 年-寒?暑?期 獸醫[\u4e00-\u9fa5]*學 第 \d{1,2} 題/')
        # 從element list 逐個取出element內部文字
        # 並存進json
        for x in lst_:
            str_ = x.text_content()
            json_container.join()
        # 返回分類瀏覽
        await page.frame(name="LBR_Body").click("img")

    # Select SUB-045
    await page.frame(name="LBR_Body").select_option(
        "select[name=\"s_Question_Subject\"]", "SUB-045")

    # Click text=送出
    await page.frame(name="LBR_Body").click("text=送出")

    # Click img
    await page.frame(name="LBR_Body").click("img")

    # Select SUB-097
    await page.frame(name="LBR_Body").select_option(
        "select[name=\"s_Question_Subject\"]", "SUB-097")

    # Click text=送出
    await page.frame(name="LBR_Body").click("text=送出")

    # Click img
    await page.frame(name="LBR_Body").click("img")

    # Close page
    await page.close()

    # ---------------------
    await context.close()
    await browser.close()

asyncio.run(main())
