from urllib.parse import urlparse


def link_parser(hrefLink):
    # Load settings
    # UNTEST
    mod = __import__('settings', {}, {}, [''])
    _settingsdict = vars(mod)
    # UNTEST
    # regex過濾url，依據url.path
    #ex: 'https://yamol.tw/exam.php?id=45082'
    urp = urlparse(hrefLink)
    if urp.path != _settingsdict['URL_FILTER_PATH']:
        return False
    else:
        return True
    # print(urp.scheme)
    # print(urp.netloc)
    # print(urp.query)


# 進入url過濾，依據內容
'td:has-text(/選擇80題/) >> a[target="_blank"]'
