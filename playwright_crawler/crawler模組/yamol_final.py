import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
import time
'''
o)先click觸發各題號，讓每題詳解ajax載入html
o)"查看全部n則討論"(n!=[0-3])須要click觸發
o)"詳解卡解鎖"須要click觸發，儲存*.html
o)"私人筆記( n )"(n=\d+)須要click觸發
o)"詳解卡解鎖"須要click觸發，儲存*_note.html
'''


async def main():
    as_pw = await async_playwright().start()
    browser = await as_pw.chromium.launch(headless=False)
    context = await browser.new_context(
        storage_state="/home/eric/文件/github/crawler_eric/cookies")
    # Doesn't effect on the timeout of actionabilities
    # context.set_default_timeout(30000)
    # Open new page
    page = await context.new_page()

    # Go to https://yamol.tw/exam.php?id=61798
    await page.goto("https://yamol.tw/exam.php?id=61798")
    time.sleep(5)
    # right panel tab N="1-50"
    list_lv0element_handle = await page.query_selector_all(
        '#item_map_tab_0 a')
    print(len(list_lv0element_handle))
    for lv0element_handle in list_lv0element_handle:
        await lv0element_handle.click(delay=2000)

    await page.click('a[href="#item_map_tab_1"]')
    list_lv1element_handle = await page.query_selector_all(
        '#item_map_tab_1 a')
    for lv1element_handle in list_lv1element_handle:
        await lv1element_handle.click(delay=2000)
    time.sleep(5)
    list_lv3element_handle = await page.query_selector_all('text=/^查看全部\s*\d+\s*則討論$/')

    for lv3element_handle in list_lv3element_handle:
        await lv3element_handle.click(delay=1300)
    time.sleep(5)
    list_lv2element_handle = await page.query_selector_all('text="詳解卡解鎖"')
    print(len(list_lv2element_handle))
    for lv2element_handle in list_lv2element_handle:
        await lv2element_handle.click(delay=3000)
    time.sleep(2)
    # save html
    title = await page.title()
    # title = [101年第二次, 105年第一次, 107 年 - 第一次, 106 年 - 第二次, 106 年 - 106-1, 109-1]
    match0 = re.search(r'(\d{2,3}\s*-\s*\d)', title)
    match1 = re.search(r'([1-9][0-9][0-9]?|第一?二?次)', title)
    if match0:
        html_body = (await page.content()).encode("utf8")
        soup = BeautifulSoup(html_body, "lxml")
        with open(f"/home/eric/文件/html_soup/{match0.group(0)}.html", "w", encoding='utf-8') as file:
            file.write(str(soup))
    elif match1:
        html_body = (await page.content()).encode("utf8")
        soup = BeautifulSoup(html_body, "lxml")
        with open(f"/home/eric/文件/html_soup/{match1.group(0)}.html", "w", encoding='utf-8') as file:
            file.write(str(soup))
    else:
        html_body = (await page.content()).encode("utf8")
        soup = BeautifulSoup(html_body, "lxml")
        with open(f"/home/eric/文件/html_soup/{title[-9:]+'_note'}.html", "w", encoding='utf-8') as file:
            file.write(str(soup))

    # 點擊私人筆記>>詳解卡解鎖>>save html
    list_lv4element_handle = await page.query_selector_all('text=/^私人筆記\(\s*\d+\s*\)$/')

    for lv4element_handle in list_lv4element_handle:
        await lv4element_handle.click(delay=3000)
    time.sleep(5)
    list_lv5element_handle = await page.query_selector_all('text="詳解卡解鎖"')
    print(len(list_lv5element_handle))
    for lv5element_handle in list_lv5element_handle:
        await lv5element_handle.click(delay=3000)
    time.sleep(5)
    # save html
    if match0:
        lv1html_body = (await page.content()).encode("utf8")
        lv1soup = BeautifulSoup(lv1html_body, "lxml")
        with open(f"/home/eric/文件/html_soup/{match0.group(0)+'_note'}.html", "w", encoding='utf-8') as file:
            file.write(str(lv1soup))
    elif match1:
        lv1html_body = (await page.content()).encode("utf8")
        lv1soup = BeautifulSoup(lv1html_body, "lxml")
        with open(f"/home/eric/文件/html_soup/{match1.group(0)+'_note'}.html", "w", encoding='utf-8') as file:
            file.write(str(lv1soup))
    else:
        lv1html_body = (await page.content()).encode("utf8")
        lv1soup = BeautifulSoup(lv1html_body, "lxml")
        with open(f"/home/eric/文件/html_soup/{title[-9:]+'_note'}.html", "w", encoding='utf-8') as file:
            file.write(str(lv1soup))

    # Close page
    await page.close()

    # ---------------------
    await context.close()
    await browser.close()

asyncio.run(main())
