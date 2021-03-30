# =========Crawler setting area===============

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Configure maximum concurrent requests performed by the crawler
CONCURRENT_REQUESTS = 2
# Maximum navigation time in milliseconds
PLAYWRIGHT_NAVIGATION_TIMEOUT = 30000
# Browser type (chromium, firefox, webkit) created when Playwright connects to a browser instance
PLAYWRIGHT_BROWSER_TYPE = 'chromium'
# Set of configurable options to set on the browser.
# See https://github.com/microsoft/playwright/blob/master/docs/api.md#browsertypelaunchoptions for description fields
# MacOS: /Users/sn_outis/Library/Caches/ms-playwright/chromium-851527/chrome-mac/Chromium.app/Contents/MacOS/Chromium
# Centos: /home/eric/.cache/ms-playwright/chromium-844399/chrome-linux/chrome
# Windows: Unknown
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,
    'executable_path': '/home/eric/.cache/ms-playwright/chromium-844399/chrome-linux/chrome',
}
USER_AGENT = 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'

DISALLOW_PATH = []

CUSTOM_ROBOT = \
    f"\nUser-agent: {USER_AGENT}\nDisallow: "

if len(DISALLOW_PATH) != 0:
    for path in DISALLOW_PATH:
        CUSTOM_ROBOT += ('\nDisallow:' + path)

# =========Filter setting area===============
# https://yamol.tw/exam.php?id=45082
# scheme= 'https', netloc= 'yamol.tw', path= '/exam.php'
# params='', query= 'id=45082', fragment=''
URL_FILTER_PATH = '/exam.php'
CONTAIN_FILTER = ''
