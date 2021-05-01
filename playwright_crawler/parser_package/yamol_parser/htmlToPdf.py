import asyncio
from playwright.async_api import async_playwright
from os.path import join
from os import walk
import argparse


'''
pdf creation only work in chromium headless mode
須提供Html資料夾所在位置(htmlpath)
    和Pdf需要存放的位置(pdfpath)

預設擷取html的列印結果，並轉換成Pdf。
不是html在螢幕上的顯示成果。
有可選模式，請指定引數。
'''
parser = argparse.ArgumentParser(description='Process Html To Pdf.')
parser.add_argument('--htmlpath', type=str, default='',
                    help='The html directory')
parser.add_argument('--pdfpath', type=str, default='',
                    help='The pdf directory')
parser.add_argument('--papersize', type=str, default='A4',
                    help='paper format: A4,B5...')
parser.add_argument('--convertmode', type=str, default='print',
                    help="mode: screen, print; Print mode: Using the style of CSS '@media print'. Screen mode: Using what's showing on the screen ")
parser.add_argument('--schemecolor', type=str, default='dark',
                    help="Default = 'dark'[ 'light', 'no-preference'] | None")
parser.add_argument('--hdfr', type=str, default='True',
                    help="Default = 'True' (Only with page-number and total number)| False")


async def html_to_pdf():
    args = parser.parse_args()
    _pw = await async_playwright().start()
    # pdf creation only work in chromium headless mode
    _browser = await _pw.chromium.launch(headless=True)
    _context = await _browser.new_context(color_scheme=f"{args.schemecolor}")
    page = await _context.new_page()
    # 對資料夾內的檔案，讀取檔名，用瀏覽器開啟檔案後產生pdf
    dir_path, _, filenames = next(walk(args.htmlpath))
    for filename in filenames:
        print(
            f"======================\n開始轉換{filename}爲Pdf\n======================")

        await page.goto(f'file://{join(dir_path, filename)}', timeout=240000)

        await page.emulate_media(media=f"{args.convertmode}", color_scheme=f"{args.schemecolor}")
        await page.pdf(
            display_header_footer=f'{args.hdfr}',
            path=f"{args.pdfpath}/{filename.split('.')[0]}.pdf",
            format=f'{args.papersize}',
            print_background=False,
            footer_template='<div style="color: lightgray; border-top: solid lightgray 1px; font-size: 10px; text-align: center; width: 100%;"><span class="title"></span> [ <span calss="pageNumber"></span> - <span class="totalPages"> ] </span></div>',
            margin={
                bottom: '2cm',
                left: '2cm',
                right: '2cm',
                top: '2cm',
            }
        )
        print(f"===========\nThe Pdf of {filename} is done...\n===========")

# ---------------------
    await page.close()
    await _context.close()
    await _browser.close()

asyncio.run(html_to_pdf())
