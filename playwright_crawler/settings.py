# =========Crawler setting===============

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Configure maximum concurrent requests performed by the crawler
CONCURRENT_REQUESTS = 2
# Maximum navigation time in milliseconds
PLAYWRIGHT_NAVIGATION_TIMEOUT = 30000
# Browser type (chromium, firefox, webkit) created when Playwright connects to a browser instance
PLAYWRIGHT_BROWSER_TYPE = 'chromium'
# Cookies storage path
# To create cookies 'playwright codegen -o gen_cookies.py https://yamol.tw/main.php --save-storage cookies'
# MacOS: '/Users/sn_outis/Documents/GitHub/playwright_crawler/playwright_crawler/cookies'
#Centos: '/home/eric/文件/github/crawler_eric/cookies'
COOKIES_PATH = '/Users/sn_outis/Documents/GitHub/playwright_crawler/playwright_crawler/cookies'
# Set of configurable options to set on the browser.
# See https://github.com/microsoft/playwright/blob/master/docs/api.md#browsertypelaunchoptions for description fields
# MacOS: /Users/sn_outis/Library/Caches/ms-playwright/chromium-851527/chrome-mac/Chromium.app/Contents/MacOS/Chromium
# Centos: /home/eric/.cache/ms-playwright/chromium-844399/chrome-linux/chrome
# Windows: Unknown
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': False,
    'executable_path': '/Users/sn_outis/Library/Caches/ms-playwright/chromium-851527/chrome-mac/Chromium.app/Contents/MacOS/Chromium'
    # 'executable_path': '/home/eric/.cache/ms-playwright/chromium-844399/chrome-linux/chrome',
}
USER_AGENT = 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'

DISALLOW_PATH = ['/fblogout.php']

CUSTOM_ROBOT = \
    f"\nUser-agent: {USER_AGENT}\nDisallow: "

if len(DISALLOW_PATH) != 0:
    for path in DISALLOW_PATH:
        CUSTOM_ROBOT += ('\nDisallow:' + path)
# ==============html(Soup) path=======
# Write the directory path(Without'/'at the end)
# MacOS: '/Users/sn_outis/Documents/GitHub/playwright_crawler/playwright_crawler'
# Centos: '/home/eric/文件/html_soup'
SOUP_PATH = '/Users/sn_outis/Documents/GitHub/playwright_crawler/playwright_crawler'

# =========Filter setting===============
# https://yamol.tw/exam.php?id=45082
# scheme= 'https', netloc= 'yamol.tw', path= '/exam.php'
# params='', query= 'id=45082', fragment=''
# str|regex
URL_FILTER_PATH = ''
URL_FILTER_PARAMS = '/\/ user -\d+.htm'
# html_contain, str|regex
# [\u4e00-\u9fa5] 匹配任何中文
# 題數
CONTAIN_FILTER_0 = '獸醫[\u4e00-\u9fa5]*學'
# 題數
CONTAIN_FILTER_1 = '選擇:80題,非選:0題'
# FIXME https://yamol.tw/fblogout.php?1617326246
# 如何排除前往這個頁面
