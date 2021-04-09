import asyncio
from playwright.async_api import async_playwright
import os
import glob


async def main():
    _pw = await async_playwright().start()
    _browser = await _pw.chromium.launch(headless=True)
    _context = await _browser.new_context()
    page = await _context.new_page()
    folder_path = '/home/eric/文件/html_soup'
    for filename in glob.glob(os.path.join(folder_path, '*.html')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            await page.setContent(f)
            await page.pdf(
                path=f'/home/eric/文件/pdf_soup/{filename}.pdf',
                format='A4',
            )
# margin = {
#     top: "20px",
#     left: "20px",
#     right: "20px",
#     bottom: "20px"
# }
