#import warnings
# warnings.filterwarnings("ignore")
import asyncio
import threading
import logging
from urllib.request import urljoin, URLError
from urllib.parse import urlparse, urlsplit, urlunsplit
from requests.structures import CaseInsensitiveDict

# https://github.com/erdewit/nest_asyncio
#import nest_asyncio
# nest_asyncio.apply()

# https://github.com/borntyping/python-colorlog
from colorlog import ColoredFormatter

# https://github.com/microsoft/playwright-python
# https://github.com/microsoft/playwright-pytest
# https://microsoft.github.io/playwright-python/async_api.html
# https://github.com/microsoft/playwright/blob/master/docs/api.md
from playwright.async_api import async_playwright, Error, TimeoutError

# https://github.com/scrapy/protego
from protego import Protego

# https://www.crummy.com/software/BeautifulSoup
from bs4 import BeautifulSoup
from .playwright_interaction import yamol_final


class PlaywrightCrawler:
    def __init__(self, base_url: str):
        # Load settings
        mod = __import__('settings', {}, {}, [''])
        self._settingsdict = vars(mod)

        self.base_url = base_url
        if isinstance(self._settingsdict['CONCURRENT_REQUESTS'], int):
            self._max_crawlers = self._settingsdict['CONCURRENT_REQUESTS']
        else:
            self._max_crawlers = 1
        self._loop = asyncio.get_event_loop()
        self._linksToCrawl = asyncio.Queue(loop=self._loop)
        self._crawledLinks = set()
        self._lock = threading.Lock()

        color_formatter = ColoredFormatter(
            (
                '%(green)s%(asctime)s%(reset)s '
                '%(log_color)s%(levelname)-7s%(reset)s '
                '%(log_color)s%(message)s%(reset)s'
            ),
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'fg_bold_red',
                'CRITICAL': 'fg_bold_red,bg_white'
            }
        )
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)-7s %(message)s', '%Y-%m-%d %H:%M:%S')
        handlerConsoleLog = logging.StreamHandler()
        handlerConsoleLog.setFormatter(color_formatter)
        handlerFileLog = logging.FileHandler(
            "playwrightCrawler.log", encoding="utf-8", mode="w")
        handlerFileLog.setFormatter(file_formatter)

        self.crawllogger = logging.getLogger(__name__)
        self.crawllogger.addHandler(handlerConsoleLog)
        self.crawllogger.addHandler(handlerFileLog)
        self.crawllogger.setLevel(logging.INFO)

        self._linksToCrawl.put_nowait(self.base_url)

    def crawl(self) -> None:
        self.crawllogger.info('[000] Crawling {}'.format(self.base_url))
        try:
            self._loop.run_until_complete(self._run())
        except KeyboardInterrupt:
            pass

    def _enqueueLinks(self, links) -> None:
        for link in links:
            # https://developer.mozilla.org/en-US/docs/Web/API/URL/href
            hrefLink = link.get('href')
            # Construct full('absolute')url with href link
            # https://docs.python.org/3/library/urllib.parse.html
            hrefLink = urljoin(self.base_url, hrefLink)
            # Remove fragment & query parameter
            hrefLink = urlunsplit(
                urlsplit(hrefLink)._replace(query="", fragment=""))
            link_url_parsed = urlparse(hrefLink)
            base_url_parsed = urlparse(self.base_url)

            # Check if a link is not crawled
            if (hrefLink in self._crawledLinks):
                continue

            # Checks if a link is internal
            if (
                (link_url_parsed.scheme != base_url_parsed.scheme)
                or (link_url_parsed.netloc != base_url_parsed.netloc)
            ):
                continue

            # Check if link target is forbidden by robots.txt

            if self._settingsdict['ROBOTSTXT_OBEY'] == True and not self._robotsTxt.can_fetch(hrefLink, "*") and not self._robotsTxt.can_fetch(hrefLink, self._settingsdict['USER_AGENT']):
                continue

            # Check if ignore the link
            # https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel#attr-nofollow
            rel = link.get('rel')
            if rel and 'nofollow' in rel:
                continue

            # Check if the path of link is target
            # 對連結進行第二層過濾，聚焦爬蟲的策略
            if self._settingsdict['URL_FILTER_PATH']:
                if link_url_parsed.path != self._settingsdict['URL_FILTER_PATH']:
                    with self._lock:
                        self._crawledLinks.add(hrefLink)
                    continue

            with self._lock:
                self._crawledLinks.add(hrefLink)
                self._linksToCrawl.put_nowait(hrefLink)

    async def _crawl(self) -> None:
        while True:
            urlToCrawl = await self._linksToCrawl.get()

            page = await self._context.new_page()
            page.on("console", lambda m: self.crawllogger.warning("[000] {} Console message : {}".format(
                m.location['url'], m.text)) if m.type in ['error'] else False)

            try:
                response = await page.goto(urlToCrawl)
                if not response.ok:
                    self.crawllogger.error('[{}] {}'.format(
                        response.status, response.request.url))
                elif response.request.redirected_from is not None:
                    redirected_from = response.request.redirected_from
                    redirected = await redirected_from.response()
                    self.crawllogger.warning('[{}] {} Redirected to {}'.format(
                        redirected.status, response.request.redirected_from.url, response.url))
                elif urlToCrawl != response.url:
                    self.crawllogger.warning(
                        '[000] Browser change url {} to {}'.format(urlToCrawl, response.url))

                if response.ok:
                    self.crawllogger.info('[{}] {}'.format(
                        response.status, response.url))
                    html_body = (await page.content()).encode("utf8")
                    soup = BeautifulSoup(html_body, "lxml")

                    # X-Robots-Tag: nofollow - Do not follow the links on this page.
                    # https://developers.google.com/search/reference/robots_meta_tag?hl=en#xrobotstag
                    headers = CaseInsensitiveDict(response.headers)
                    if headers.get('x-robots-tag') and 'nofollow' in headers.get('x-robots-tag'):
                        self.crawllogger.warning(
                            'X-Robots-Tag HTTP header: nofollow on {}'.format(response.url))
                    else:
                        # robots meta tag: nofollow - Do not follow the links on this page.
                        # https://developers.google.com/search/reference/robots_meta_tag?hl=en#robotsmeta
                        metarobots = await page.query_selector("meta[name=robots]")
                        metacontent = ''
                        if metarobots:
                            metacontent = await metarobots.get_attribute('content')
                        if 'nofollow' in metacontent:
                            self.crawllogger.warning(
                                'Robots meta tag: nofollow on {}'.format(response.url))
                        else:
                            # 對內容進行第一層過濾，從寬度爬蟲轉換成聚焦爬蟲
                            contain_filter_0 = self._settingsdict['CONTAIN_FILTER_0']
                            contain_filter_1 = self._settingsdict['CONTAIN_FILTER_1']
                            # 防止FILTER爲'空',還執行代碼降低效率
                            if len(contain_filter_0) != 0 or len(contain_filter_1) != 0:
                                list_contain_filter = await page.query_selector(
                                    f'text=/{contain_filter_0}/ >> text=/{contain_filter_1}/')
                                # 防止網頁內容沒有'關注內容'，還執行代碼降低效率
                                if list_contain_filter:
                                    # 抓取關注內容頁面中所有連結
                                    self._enqueueLinks(soup.find_all('a'))
                                    # 進入互動模組
                                    try:
                                        yamol_final.main(page)
                                    # 無法滿足互動條件，跳出本次迴圈
                                    except:
                                        continue
                            # 抓取沒有關注內容的頁面中所有連結
                            self._enqueueLinks(soup.find_all('a'))

                with self._lock:
                    self._crawledLinks.add(response.url)

            except (TimeoutError) as te:
                self.crawllogger.error('{} {}'.format(
                    urlToCrawl, te.message.split('.')[0]))
            except (Error) as te:
                self.crawllogger.error('{} {}'.format(
                    urlToCrawl, te.message.split('.')[0]))
            finally:
                await page.close()

            self._linksToCrawl.task_done()

    async def _run(self) -> None:
        await self._lauch_browser()

        crawlers = [
            asyncio.create_task(self._crawl()) for _ in range(self._max_crawlers)
        ]

        await self._linksToCrawl.join()
        for c in crawlers:
            c.cancel()

        await self._close()

    async def _close(self) -> None:
        if hasattr(self, '_browser'):
            await self._browser.close()
        await self._pw.stop()
        self.crawllogger.info('[000] Crawl finished')

    def close(self) -> None:
        self._loop.run_until_complete(self._close())

    async def _lauch_browser(self) -> None:
        self._pw = await async_playwright().start()
        pwOptions = self._settingsdict['PLAYWRIGHT_LAUNCH_OPTIONS']
        if not "".__eq__(self._settingsdict['PLAYWRIGHT_BROWSER_TYPE']):
            if self._settingsdict['PLAYWRIGHT_BROWSER_TYPE'] not in ['chromium', 'firefox', 'webkit']:
                raise RuntimeError(
                    'Invalid PLAYWRIGHT_BROWSER_TYPE configuration')

            if self._settingsdict['PLAYWRIGHT_BROWSER_TYPE'] == 'chromium':
                self._browser = await self._pw.chromium.launch(**pwOptions)
            elif self._settingsdict['PLAYWRIGHT_BROWSER_TYPE'] == 'firefox':
                self._browser = await self._pw.firefox.launch(**pwOptions)
            elif self._settingsdict['PLAYWRIGHT_BROWSER_TYPE'] == 'webkit':
                self._browser = await self._pw.webkit.launch(**pwOptions)
        # If no Cookies path is provided, storage state is still returned, but won't be saved to the disk
        self._context = await self._browser.new_context(user_agent=self._settingsdict['USER_AGENT'], storage_state=self._settingsdict['COOKIES_PATH'])

        self._context.set_default_navigation_timeout(
            self._settingsdict['PLAYWRIGHT_NAVIGATION_TIMEOUT'])

        blankPage = await self._context.new_page()
        getUA = await blankPage.evaluate('''() => {
          return navigator.userAgent
        }''')

        # Load robots.txt file
        response = await blankPage.goto(urlparse(self.base_url).scheme + '://' + urlparse(self.base_url).netloc + '/robots.txt')
        if response.ok:
            try:
                text = await blankPage.inner_text('pre')
            except TimeoutError as e:
                print('my print', e)
                text = await blankPage.inner_text('body')
            text = text + self._settingsdict['CUSTOM_ROBOT']
            res = Protego.parse(text)

            self._robotsTxt = res
        else:
            self._robotsTxt = Protego.parse("""
          User-agent: *
          Allow: /
          """)

        self.crawllogger.info(
            '[000] Starting browser with User Agent: {}'.format(getUA))


dir = dir()
__objname__ = [o for o in dir if not '__' in o]
