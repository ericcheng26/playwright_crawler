import asyncio
from playwright.async_api import async_playwright

click_target_lv0 = ["獸醫病理學", "獸醫藥理學",
                    "獸醫實驗診斷學", "獸醫普通疾病學", "獸醫傳染病學", "獸醫公共衛生學"]
click_target_lv1 = ["詳解卡解鎖", "私人筆記( 1 )"]


async def run(playwright):
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()

    # Open new page
    page = await context.new_page()

    # Go to https://yamol.tw/examinfo.php
    await page.goto("https://yamol.tw/examinfo.php")
    # Click text="獸醫病理學"
    page.click("text=\"獸醫病理學\"")
    # assert page.url == "https://yamol.tw/cat.php?id=1895"
    list_lv0element_handle = page.query_selector_all("text=\"私人筆記( (?!0))\"")
    while True:
        try:
            for lv0element_handle in list_lv0element_handle:
                lv0element_handle.click()
        except:
            break
    list_lv1element_handle = page.query_selector_all("text=\"詳解卡解鎖\"")
    while True:
        try:
            for lv1element_handle in list_lv1element_handle:
                lv1element_handle.click()
        except:
            break

    # Close page
    await page.close()

    # ---------------------
    await context.storage_state(path="/home/eric/文件/cookies")
    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
