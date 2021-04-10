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
parser.add_argument('-hp', dest='htmlpath',
                    help='Fill the html directory')
parser.add_argument('-pp', dest='pdfpath',
                    help='Fill the pdf directory')
args = parser.parse_args()
htmlpath = args.htmlpath
pdfpath = args.pdfpath


async def main(htmlpath, pdfpath):
    _pw = await async_playwright().start()
    # pdf creation only work in chromium headless mode
    _browser = await _pw.chromium.launch(headless=True)
    _context = await _browser.new_context()
    page = await _context.new_page()
    # 對資料夾內的檔案，讀取和產生pdf
    for filename in glob.glob(os.path.join(htmlpath, '*.html')):
        with open(os.path.join(htmlpath, filename), 'r') as f:
            await page.setContent(f)
            await page.emulate_media(media="screen", color_scheme="dark")
            await page.pdf(
                path=f'{pdfpath}/{filename}.pdf',
                format='A4'
            )
# margin = {
#     top: "20px",
#     left: "20px",
#     right: "20px",
#     bottom: "20px"
# }
