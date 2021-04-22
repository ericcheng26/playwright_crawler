import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import time
import random
'''
o)先click觸發各題號，讓每題詳解ajax載入html
o)"查看全部n則討論"(n!=[0-3])須要click觸發
o)"詳解卡解鎖"須要click觸發，儲存*.html
o)"私人筆記( n )"(n=\d+)須要click觸發
o)"詳解卡解鎖"須要click觸發，儲存*_note.html
'''


async def main(page, _settingsdict):
    time.sleep(1)
    # right panel tab N="1-50"
    list_lv0element_handle = await page.query_selector_all(
        '#item_map_tab_0 a')
    for lv0element_handle in list_lv0element_handle:
        await lv0element_handle.click(delay=3000)
        time.sleep(1)
        # Press PageDown
        try:
            await page.press("body", "PageDown", delay=25)

        except:
            await page.press(
                "body:has-text(\"× 載入中..請稍候.. 關閉 通知 Mark as Read Templates Synced 20 Templates have been synced t\")", "PageDown", delay=25)

            # right panel tab N="51-100"
    await page.click('a[href="#item_map_tab_1"]')
    list_lv1element_handle = await page.query_selector_all(
        '#item_map_tab_1 a')
    for lv1element_handle in list_lv1element_handle:
        await lv1element_handle.click(delay=3000)
        time.sleep(1)
        # Press PageDown
        try:
            await page.press("body", "PageDown", delay=25)

        except:
            await page.press(
                "body:has-text(\"× 載入中..請稍候.. 關閉 通知 Mark as Read Templates Synced 20 Templates have been synced t\")", "PageDown", delay=25)

    time.sleep(2)
    # prepare to save html's file name
    title = await page.title()
    str_subject_name = (await (await page.query_selector('text=/獸醫[\u4e00-\u9fa5]*學/')).text_content())[3:-4]

    # ready for file name
    # title = [101年第二次, 105年第一次, 107 年 - 第一次, 106 年 - 第二次, 106 年 - 106-1, 109-1]
    match1 = re.match(
        r"(^[1-9][0-9][0-9]?)[^第0-9]*(\d{2,3}\s*-\s*\d)?[^第]*(第一?二?次)?", title)
    if match1:
        if match1.group(2):
            html_file_name = f"{_settingsdict['SOUP_PATH']}/{match1.group(2)}_{str_subject_name}"
        else:
            html_file_name = f"{_settingsdict['SOUP_PATH']}/{match1.group(1)}_{match1.group(3) + '_' if match1.group(3) else ''}{str_subject_name}"
    else:
        html_file_name = f"{_settingsdict['SOUP_PATH']}/{title[-9:]}_{str_subject_name}"

    # 點擊的按鈕可能已經被點擊過，所以沒有任何按鈕可以按，會TimeoutError
    try:
        list_lv3element_handle = await page.query_selector_all('text=/^查看全部\s*\d+\s*則討論$/')
        for lv3element_handle in list_lv3element_handle:
            await lv3element_handle.click(delay=3000)

        time.sleep(3)
        list_lv2element_handle = await page.query_selector_all('text="詳解卡解鎖"')
        print(len(list_lv2element_handle))
        time.sleep(1)
        for lv2element_handle in list_lv2element_handle:
            await lv2element_handle.click(delay=3000)
    except:
        print('查看全部n則討論|詳解卡解鎖無按鈕可按')
    # save html file, file name depend on match result
    with open(html_file_name + '.html', "w", encoding='utf-8') as file:
        file.write(str(BeautifulSoup((await page.content()).encode("utf8"), "lxml")))
    time.sleep(1)
    # 點擊私人筆記>>詳解卡解鎖>>save html
    list_lv4element_handle = await page.query_selector_all('text=/^私人筆記\(\s*\d+\s*\)$/')
    for lv4element_handle in list_lv4element_handle:
        await lv4element_handle.click(delay=3000)
    time.sleep(3)
    # 私人筆記中的詳解卡解鎖可能無東西可按
    try:
        list_lv5element_handle = await page.query_selector_all('text="詳解卡解鎖"')
        print(len(list_lv5element_handle))
        for lv5element_handle in list_lv5element_handle:
            await lv5element_handle.click(delay=3000)
    except:
        print('私人筆記中的詳解卡解鎖無按鈕可按')
    # save html file, file name depend on match result
    with open(html_file_name + '_note.html', "w", encoding='utf-8') as file:
        file.write(str(BeautifulSoup((await page.content()).encode("utf8"), "lxml")))
