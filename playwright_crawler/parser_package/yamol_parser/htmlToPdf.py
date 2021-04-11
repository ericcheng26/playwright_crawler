import asyncio
from playwright.async_api import async_playwright
import os
import glob
import argparse

'''
pdf creation only work in chromium headless mode
須提供Html資料夾所在位置(htmlpath)
    和Pdf需要存放的位置(pdfpath)
'''
parser = argparse.ArgumentParser(description='Process Html To Pdf.')
parser.add_argument('--htmlpath', type=str, default='',
                    help='The html directory')
parser.add_argument('--pdfpath', type=str, default='',
                    help='The pdf directory')
parser.add_argument('--papersize', type=str, default='',
                    help='paper format: A4,B5...')


async def main():
    args = parser.parse_args()
    _pw = await async_playwright().start()
    # pdf creation only work in chromium headless mode
    _browser = await _pw.chromium.launch(headless=True)
    _context = await _browser.new_context()
    page = await _context.new_page()
    # 對資料夾內的檔案，讀取和產生pdf
    for filename in glob.glob(os.path.join(args.htmlpath, '*.html')):

        await page.goto(os.path.join(args.htmlpath, filename))
        await page.emulate_media(media="screen", color_scheme="dark")
        await page.pdf(
            path=f'{args.pdfpath}/{filename}.pdf',
            format=f'{args.papersize}'
        )
# margin = {
#     top: "20px",
#     left: "20px",
#     right: "20px",
#     bottom: "20px"
# }
