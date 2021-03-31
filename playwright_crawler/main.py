
import sys
from optparse import OptionParser

from crawler_package import PlaywrightCrawler
# from parser_package import
__version__ = "0.2"

if __name__ == '__main__':
    parser: OptionParser = OptionParser(
        usage="%prog <url>", version="v" + __version__)
    opts, args = parser.parse_args()
    if len(args) < 1:
        parser.print_help(sys.stderr)
        raise SystemExit(1)

    pwc: PlaywrightCrawler = None
    try:
        pwc = PlaywrightCrawler(args[0])
        pwc.crawl()
    except Exception as ex:
        if pwc:
            pwc.crawllogger.error(ex)
            pwc.close()
        else:
            print('ERROR: ', ex)
