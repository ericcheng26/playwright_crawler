from urllib.parse import urlparse


def link_parser(hrefLink):
    # regex過濾url，依據url.path
    #ex: 'https://yamol.tw/exam.php?id=45082'
    urp = urlparse(hrefLink)
    if urp.path != '/exam.php':
        return False
    else:
        return True
    # print(urp.scheme)
    # print(urp.netloc)
    # print(urp.path)
    # print(urp.params)
    # print(urp.query)
    # print(urp.fragment)


# Css過濾內部url，依據內容
'td:has-text(/選擇80題/) >> a[target="_blank"]'
