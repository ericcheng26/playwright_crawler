import asyncio
from playwright.async_api import async_playwright
import os
import glob
import argparse

'''
pdf convert only work in chromium headless mode
須提供Html資料夾所在位置(html_folder_path)
    和Pdf需要存放的位置(pdf_folder_path)
'''
parser = argparse.ArgumentParser(description='Process Html To Pdf.')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='')
args = parser.parse_args()


async def main(html_folder_path, pdf_folder_path):
    _pw = await async_playwright().start()
    # pdf convert only work in chromium headless mode
    _browser = await _pw.chromium.launch(headless=True)
    _context = await _browser.new_context()
    page = await _context.new_page()
    html_folder_path = '/home/eric/文件/html_soup'
    for filename in glob.glob(os.path.join(html_folder_path, '*.html')):
        with open(os.path.join(html_folder_path, filename), 'r') as f:
            await page.setContent(f)
            await page.emulate_media(media="screen", color_scheme="dark")
            await page.pdf(
                path=f'{pdf_folder_path}/{filename}.pdf',
                format='A4'
            )
# margin = {
#     top: "20px",
#     left: "20px",
#     right: "20px",
#     bottom: "20px"
# }
