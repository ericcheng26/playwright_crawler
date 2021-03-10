# playwright-webcrawler

Parallel crawler powered by Headless browser ([Chromium](https://www.chromium.org/Home), [Firefox](https://www.mozilla.org/en-US/firefox/new/) and [WebKit](https://webkit.org/))

## Features

Crawlers based on simple requests to HTML files are generally fast. However, it sometimes ends up capturing empty bodies, especially when the websites require JS to function properly and to make the scraper more similar to humans.

playwright-webcrawler is intended to be used for parallel crawling of web pages using headless browser with [playwright-python](https://github.com/microsoft/playwright-python).

|          | Linux | macOS | Windows |
|   :---   | :---: | :---: | :---:   |
| Chromium <!-- GEN:chromium-version -->86.0.4238.0<!-- GEN:stop --> | ✅ | ✅ | ✅ |
| WebKit 14.0 | ✅ | ✅ | ✅ |
| Firefox <!-- GEN:firefox-version -->80.0b8<!-- GEN:stop --> | ✅ | ✅ | ✅ |

Headless execution is supported for all browsers on all platforms.

## Installation

playwright-webcrawler uses Python 3 (lowest version tested is 3.7.0).

Install requirements:

    pip install -r requirements.txt

> **Note**: playwright-webcrawler contains [Playwright for Python](https://github.com/microsoft/playwright-python). If you want to downloads a recent version of browsers binaries for Chromium, Firefox and WebKit, you must do:

    python -m playwright install

## Configuration file

playwright-webcrawler uses configuration files `settings.py` in order to store all configuration options.

* ROBOTSTXT_OBEY

    If True, playwright-webcrawler will respect robots.txt policies.

* CONCURRENT_REQUESTS

    The maximum number of concurrent (i.e. simultaneous) requests that will be performed by the crwler.

* PLAYWRIGHT_NAVIGATION_TIMEOUT = 30000

    The amount of time (in millisecs) that the browser will wait before timing out.

* PLAYWRIGHT_BROWSER_TYPE

    Browser type (chromium, firefox, webkit) created when Playwright connects to a browser instance.

* PLAYWRIGHT_LAUNCH_OPTIONS

    Set of configurable options to set on the browser.
    See [browserType.launch([options])](https://github.com/microsoft/playwright/blob/master/docs/api.md#browsertypelaunchoptions) for description fields

## Usage

1. Once your configuration file is saved, simply launch your first crawl: `python main.py <url>`
2. Wait it crawls the whole webiste or exit using `^C`

## How is this different from Playwright?

This crawler is built on top of [Playwright for Python](https://github.com/microsoft/playwright-python).

Playwright for Python provides low to mid level APIs to manupulate headless browser, so you can build your own crawler with it. This way you have more controls on what features to implement in order to satisfy your needs.

However, most crawlers requires such common features as following links, obeying [robots.txt](https://developers.google.com/search/reference/robots_txt) and etc.

This crawler is a general solution for most crawling purposes. If you want to quickly start crawling with headless browser, this crawler is for you.

## Contributing

If you wish to contribute to this repository or to report an issue, please do this [on Github issues](https://github.com/LeMoussel/playwright-webcrawler/issues).
