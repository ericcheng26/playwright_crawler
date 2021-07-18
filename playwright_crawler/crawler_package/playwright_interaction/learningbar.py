import asyncio
from playwright.async_api import async_playwright
import time


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
    # Press Tab
    await page.frame(name="LBR_Body").press("[placeholder=\"Password\"]", "Tab")

    Verification_word = input('請輸入驗證碼')
    await page.frame(name="LBR_Body").fill("[placeholder=\"請在此輸入驗證碼\"]", f"{Verification_word}")

    # Click input:has-text("登入")
    await page.frame(name="LBR_Body").click("input:has-text(\"登入\")")

    # 每次先選擇不同類別，再做相同行爲
    # 行爲=抓取所有"出處xxxx"的element，然後將文字取出
    # 嘗試：取出文字後下一頁，並執行"行爲"，直到沒有目標
    # 分類號碼從44~97
    for x in range(44, 98):
        # Click text=分類瀏覽
        await page.frame(name="LBR_Body").click("text=分類瀏覽")

        await page.frame(name="LBR_Body").select_option("select[name=\"s_Question_Subject\"]", f"SUB-0{x}")

        await page.frame(name="LBR_Body").click("text=送出")
        print('wait 18sec, cause server too bird')
        time.sleep(18)
        # 找出含有"出處: 民國xxxxx" 的element並用list裝起來
        list_lv0element_handle = page.frame(name="LBR_Body").query_selector_all(
            'text=/出處: 民國 \d{2,3} 年-寒?暑?期 獸醫[\u4e00-\u9fa5]*學 第 \d{1,2} 題/')
        # 從element list 逐個取出element內部文字
        # 並存進json
        try:
            while True:
                await page.frame(name="LBR_Body").click("text=下一頁")
                print('wait 18sec, cause server too bird')
                time.sleep(18)
                list_lv1element_handle = page.frame(name="LBR_Body").query_selector_all(
                    'text=/出處: 民國 \d{2,3} 年-寒?暑?期 獸醫[\u4e00-\u9fa5]*學 第 \d{1,2} 題/')
                list_lv0element_handle = list_lv0element_handle+list_lv1element_handle
        except:
            pass

        # Click text=作答平台
        page.frame(name="LBR_Banner").click("text=作答平台")

    # Close page
    await page.close()

    # ---------------------
    await context.close()
    await browser.close()

asyncio.run(main())
