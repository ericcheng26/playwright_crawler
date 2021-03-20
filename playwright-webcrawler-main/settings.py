# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Configure maximum concurrent requests performed by the crawler
CONCURRENT_REQUESTS = 5
# Maximum navigation time in milliseconds
PLAYWRIGHT_NAVIGATION_TIMEOUT = 30000
# Browser type (chromium, firefox, webkit) created when Playwright connects to a browser instance
PLAYWRIGHT_BROWSER_TYPE = 'chromium'
# Set of configurable options to set on the browser.
# See https://github.com/microsoft/playwright/blob/master/docs/api.md#browsertypelaunchoptions for description fields
PLAYWRIGHT_LAUNCH_OPTIONS = {
  'headless': False,
  'executablePath': 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
}
