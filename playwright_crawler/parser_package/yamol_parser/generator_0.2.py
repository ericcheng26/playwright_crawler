from os.path import isabs, isfile, isdir, basename, dirname, join
from os import makedirs, listdir, walk
from json import load
from bs4 import BeautifulSoup as BS
import requests
import re
import base64


def url_to_base64(url):
    raw = requests.get(
        'http://www.chemspider.com/ImagesHandler.ashx?id=8894&w=250&h=250').content
    b64data = base64.b64encode(raw)[2:-1]
    return '<img src="data:image/jpeg;base64, ' + b64data + '>'


def img_to_base64(img_path):
    with open(img_path, 'rb') as f:
        raw = f.read()
    b64data = base64.b64encode(raw)[2:-1]
    return '<img src="data:image/jpeg;base64, ' + b64data + '">'


def q_part_generator(q_list):
    result = '''    <table class="main_block">
    <tr>
      <td class="q_and_c">'''
    result += q_list[0]

    for c in q_list[1]:
        result += ('<br>' + c)

    result += '</td>'

    try:
        for img_path in q_list[3]:
            image = img_to_base64(img_path)
            result += ('<td class="q_image">' + image + '</td>')
    except:
        pass

    result += '</tr></table>'

    result += '<table class="ans_block"><tr><td class="ans_head">答案</td><td class="ans_val">%s</td></tr></table>' % q_list[2]
    return result


def d_part_generator(d_tag_list=None, n_tag_list=None):
    result = '<div class="note_and_discussion">'
    if d_tag_list != None and d_tag_list != []:
        result += '<h2 class="d_n_title">詳 解</h2>'

        for tag in d_tag_list:
            result += str(tag)

    if n_tag_list != None and n_tag_list != []:
        result += '<h2 class="d_n_title">筆 記</h2>'

        for tag in n_tag_list:
            result += str(tag)

    result += '</div>'
    return result


# 給定單獨的json路徑
def generator(single_json_path):

    title = basename(single_json_path).replace('.json', '')
    dir_path = dirname(single_json_path)
    static_path = join(dir_path, 'static')
    discussion_path = join(static_path, 'discussion.html')
    note_path = join(static_path, 'note.html')

    if isfile(discussion_path):
        with open(discussion_path, 'r', encoding='utf-8') as f:
            d_soup = BS(f.read(), 'lxml')
    else:
        d_soup = None

    if isfile(note_path):
        with open(note_path, 'r', encoding='utf-8') as f:
            n_soup = BS(f.read(), 'lxml')
    else:
        n_soup = None
# 生成html內head和body區塊
    result = '''\
    <style>
    body {
      margin: 0;
      padding: 0;
      background-color: gray;
      font-family: arial,"Microsoft JhengHei","微軟正黑體",sans-serif !important;
    }

    div.block{
      margin: auto;
      background-color: #f7f7e6;
      width: 21.5cm;
      padding: 1cm;
    }

    h1.d_number {
      display: inline-block;
      font-family: serif;
      font-style: italic;
      font-size: 14pt;
      border-radius: 18px;
      background-color: LightGray;
      padding: 0.2cm;
      margin-block-start: 0em;
      margin-block-end: 0.1em;
      margin-inline-start: 0px;
      margin-inline-end: 0px;
    }

    h1.main_head{
      display: block;
      background-color: cyan;
      padding: 0.5cm;
      border-style: double;
      border-width: 0.25cm;
      text-align: center;
      font-weight: bold;
    }

    table.contents{
      border: 1px solid black;
      }

    a.head_contents{
      font-size:0.7cm;
      border-radius: 18px;
      background-color:LightGray;
      display: flex;
      flex-direction: row;
      justify-content: space-evenly;
      font-weight: bold;
    }

    thead{
      height:2cm;
    }

    td.inner_contents{
      border: 1.5px solid black;
      width: 1cm;
      background-color: LightYellow;
      text-align: center;
    }

    div.q_block{
      margin: 0.5cm 0 0 0;
      border-top: 5px solid black;
      border-bottom: 5px double black;
      padding:0cm;
    }

    hr{
      display: table-cell;
      unicode-bidi: isolate;
      margin-block-start: 0.1em;
      margin-block-end: 0.5em;
      margin-inline-start: auto;
      margin-inline-end: auto;
      overflow: hidden;
      border-style: inherit;
      border-width: 0.1px;
    }

    h2{
      margin-block-start: 0.1em;
      margin-block-end: 0.1em;
      margin-inline-start: 0px;
      margin-inline-end: 0px;
    }

    h2.d_n_title {
      display: block;
      font-size: 15pt;
      text-align-last: center;
    }

    h2.qid{
      border-radius: 18px;
      background-color: LightGray;
      margin: 0cm 0 0.1cm 0;
      text-align-last: center;
      font-size: xx-large;
    }

    .alert {
      display: table;
      table-layout: fixed;
      width: -webkit-fill-available;
      font-family: serif;
      font-size: 12pt;
    }

    table {
      border-collapse:collapse;
      width: 100%;
    }

    .table-bordered {
      border: 1px solid #b3b3b3;
      border-top-color: rgb(179, 179, 179);
      border-top-style: solid;
      border-top-width: 1px;
      border-right-color: rgb(179, 179, 179);
      border-right-style: solid;
      border-right-width: 1px;
      border-bottom-color: rgb(179, 179, 179);
      border-bottom-style: solid;
      border-bottom-width: 1px;
      border-left-color: rgb(179, 179, 179);
      border-left-style: solid;
      border-left-width: 1px;
      border-image-source: initial;
      border-image-slice: initial;
      border-image-width: initial;
      border-image-outset: initial;
      border-image-repeat: initial;
    }

    table.main_block{
      border-radius: 20px;
      width:100%;
      background-color: LightYellow;
      margin:0.1cm 0 0.3cm 0;
    }
    td {
      border-collapse:collapse;
      border: 1px solid;
      border-color: darkslategrey;
    }

    tr{
      border-collapse: collapse;
      border: 1px solid;
      border-color: darkslategrey;
    }

    img {
      min-width: -webkit-fill-available;
      max-width: 100%;
      height: auto;
    }

    table.ans_block{
      border-radius: 20px;
      border-color: darkslategrey;
      margin:0.1cm 0 0.3cm 0;
      width:100%;
    }

    td.q_and_c{
      border: hidden;
    }

    td.ans_head{
      font-weight: bold;
      text-align: center;
    }

    td.ans_val{
      text-align: center;
    }

    div.note_and_discussion{
      width: 100%;
      margin-bottom: 0.2cm;
    }

    @page{
      size: A4 portrait;
      margin: 2cm;
      widows:2;
      orphans:4;
    }

    @media print{
      header nav, footer, video, audio, object, embed {
        display: none;
      }
      body{
        -webkit-print-color-adjust: economy;
        background-color: #fff !important;
        color: #000;
        width: 100%;
        margin: 0;
        float: none;
        line-height: 1.3;
        font-size: 12pt;
        font-family:serif;
      }

      a.head_contents{
        display:none;
      }

      td.inner_contents{
        display:none;
      }

      div{
        background-color: #fff;
        -webkit-box-decoration-break: clone;
      }

      table.ans_block{
        border: 1px solid;
        border-color: #000000;
        border-radius: 20px;
      }

      h1.main_head{
        padding: 0cm;
        text-align: center;
        font-weight: bold;
      }

      h1.d_number{
        background-color: LightGray !important;
      }

      img {
        min-width: -webkit-fill-available;
        max-width: 100%;
        height: auto;
        filter: url(inverse.svg#negative);
        -webkit-filter: invert(100%);
        filter: invert(100%);
      }

      a:link, a:visited, a {
        background: transparent;
        color: #520;
        font-weight: bold;
        text-decoration: underline;
        text-align: left;
        word-wrap: break-word; /*避免網址過長超出頁面*/
      }


      thead{
        display: table-header-group; /* 表格即使分頁也會顯示表頭 */
      }

      h2, h3, h4, h5, h6 {
        page-break-before:auto;
        page-break-inside:avoid;
      }

      h2.d_n_title {
        page-break-after:avoid;
      }

      h2+p, h3+p {
        page-break-before: avoid;
      }

      a {
        page-break-inside:avoid;
      }

      img{
        page-break-inside: avoid;
      }

      table, blockquote{
        page-break-before: avoid;
      }

      table.ans_block{
        page-break-inside: avoid;
      }

      table.main_block{
        page-break-inside: avoid;
      }
      
      td.q_and_c{
        page-break-inside: avoid;
      }

      ul, ol, dl {
        page-break-before:avoid;
      }

      div.note_and_discussion{
        page-break-before: auto;
        -webkit-box-decoration-break: clone;
      }
    }
  </style>

  <body>

  <div class=block>

  <h1 class=main_head>
    我是標題
  </h1>

  <div style="margin:0 0 0.3cm 0;"><a name=contents class=head_contents>目 錄</a></div>
    <table class=contents >
    <tr>\
  '''.replace('我是標題', title)
# 生成html內目錄區塊
    for i in range(1, 81):

        result += '<td class=inner_contents><a href=#%d>%d</a></td>' % (i, i)

        if (i % 20 == 0) and i != 80:
            result += '''
      </tr>
      <tr>
      '''
        elif i == 80:
            result += '''
      </tr>
    </table>
      '''
# 生成詳解討論和筆記區塊
    with open(single_json_path, 'r', encoding='utf-8') as f:
        json_dict = load(f)

    for i in range(1, 81):
        i = str(i)

        result += '''
    <div class="q_block %s">
    <hr></hr>
    <h2 class="qid"><a name=%s  href=#contents>%s.</a></h2>
    ''' % (i, i, i)

        q_list = json_dict[i]
        result += q_part_generator(q_list)

        d_tag_list = d_soup.select(
            f'div[class^="{i}-"]') if d_soup != None else None
        n_tag_list = n_soup.select(
            f'div[class^="{i}-"]') if n_soup != None else None

        result += d_part_generator(d_tag_list, n_tag_list)

        result += '\n</div>\n'

    result += '</div></body>'
    # TODO replace a list of substring in string
    result = result.replace('<p></p>', '').replace('<p><span></span></p>', '').replace('<p><b></b></p>', '').replace(
        '<p><span><br/></span><br/></p>', '').replace('<p><span><br/></span></p>', '').replace('&nbsp;', '').strip()
    return result, title
# <p><span style="font-size:20px;"><br></span></p>
# <p><font><br></font></p>
# <p><font color="#222222"><b><br></b></font></p>
# <p><span style="color:rgb(80,78,78);"><br></span></p>
# <p><font color="#3152a9"><span style="background-color:rgb(255,255,255);font-size:11.7px;"><br></span></font></p>
# <p></p>
# <p><span style="color:rgb(34,34,34);"><br></span></p>
# <p><span></span></p>
# <p><b></b></p>
# <p><spastyle><br><br></spastyle></p>
# <p><span><br/></span><br/></p>
# <p><span><br/></span></p>
# 批量把str儲存成html檔


def quick_generator(json_path, html_combined_path):
    # 取出json_path中最上層資料夾的絕對路徑(dirpath)和資料夾名稱(dirnames)
    dirpath, dirnames, _ = next(walk(json_path))
    # 只須放入"*note"的資料夾
    lv1_dirnames = [dname for dname in dirnames if dname.endswith('note')]
    # 開始批次存檔
    for dirname in lv1_dirnames:
        str_combined_html, combined_filename = generator(
            join(dirpath, join(dirname, dirname + '.json')))
        try:
            with open(f"{html_combined_path}/{combined_filename.removesuffix('_note')}.html", 'x', encoding='utf-8') as f:
                f.write(str_combined_html)
                print(
                    f"===========\nThe Combination of \"{combined_filename.removesuffix('_note')}\" is done.\n===========")
        except FileExistsError:
            print(
                f"===========\nThe path \"{html_combined_path}\" already exist {combined_filename.removesuffix('_note')}.html.\n===========")


def RemoveRedundantTag(html_soup_path):
    dirpath, _, filenames = next(walk(html_soup_path))
    # tag_whitelist = ['head', 'img', 'br', 'tr', 'td']
    for filename in filenames:
        with open(join(dirpath, filename), 'r+', encoding='utf-8') as f:
            soup = BS(f.read(), 'lxml')
            [x.decompose() for x in soup.findAll(lambda tag: (not tag.contents or not tag.get_text(
                strip=True)) and tag.name != 'head', 'img', 'br', 'tr', 'td')]
            f.seek(0)
            f.write(" ".join(str(soup).replace('&nbsp;', '').split()))

            f.truncate()
        print(
            f"===========\nRemove Redundant Tag \"{filename}\" Complete.\n===========")


def RemoveRedundantString(html_soup_path):
    dirpath, _, filenames = next(walk(html_soup_path))

    for filename in filenames:
        with open(join(dirpath, filename), 'r+', encoding='utf-8') as f:
            bad_string_free_html = f.read().replace(
                '<p><span style="background-color:rgb(255,255,0);"><br/></span></p>', '').replace(
                '<p style="color:rgb(51,51,51);"><br/></p>', '').replace(
                '<p><font color="#222222"><b><br/></b></font></p>', '').replace(
                '<p><span style="color:rgb(51,51,51);font-size:14.4px;"><br/></span></p>', '').replace(
                '<p><span style="color:rgb(34,34,34);"><br/></span></p>', '').replace(
                '<p> </p>', '').replace(
                '<p><span style="background-color:rgb(245,245,245);"><br/></span></p>', '').replace(
                '<p><span style="color:rgb(34,34,34);"><br/></span><br/></p>', '').replace(
                '<p><span style="color:rgb(51,51,51);"><br/></span></p>', '').replace(
                '<p style="color:rgb(34,34,34);"><br/></p>', '').replace('<p><font color="#3152a9"><span style="background-color:rgb(255,255,255);font-size:11.7px;"><br/></span></font></p>', '').replace('<p><span style="color:rgb(34,34,34);"><br/></span></p>', '').replace('<p><spastyle><br/><br/></spastyle></p>', '').replace('<p><font><br/></font></p>', '').replace('<p><span style="font-size:20px;"><br/></span></p>', '').replace('<p style="color:rgb(68,68,68);"><br/></p>', '').replace('<p><span style="color:rgb(68,68,68);"><br/></span></p>', '').replace('<p><span style="font-size:1.1em;"><br/></span></p>', '').replace('<p><span style="color:rgb(51,51,51);font-size:14pt;"><br/></span></p>', '').replace('<span style="font-size:1.1em;"><br/></span>', '').replace('<span style="font-size:16.94px;"><br/></span>', '').replace('<p><b><span style="font-size:14px;"><br/></span></b></p>', '').replace('<p style="font-size:12pt;"> </p>', '').replace('<p><span style="font-size:15.4px;"><br/></span></p>', '').replace('<p><span style="font-size:15.4px;"><br/></span><br/></p>', '').replace('<p><span style="font-size:15.6px;"><br/></span><br/></p>', '').replace('<div><br/></div>', '').replace('<p><span style="color:rgb(17,17,17);"><br/></span></p>', '').replace('<span><br/></span>', '').replace('<p> <br/></p>', '').replace('<h4><br/></h4>', '').replace('<p style="color:rgb(0,0,0);"><br/></p>', '').replace('<p><br/><br/><br/></p>', '').replace("<p><span style=\"font-family:'微軟正黑體';\"><br/></span><br/></p>", '').replace("<p style=\"font-family:'微軟正黑體';font-size:12pt;\"><span style=\"font-weight:bold;color:rgb(91,155,213);\"><br/></span></p>", '').replace('<p><span style="color:rgb(85,85,85);"><br/></span></p>', '').replace('<p><br/></p>', '').replace('<p><span style="color:rgb(80,78,78);"><br/></span></p>', '').replace('<p><span style="color:rgb(80,78,78);background-color:rgb(247,247,247);"><br/></span><br/></p>', '').replace('<span style="color:rgb(34,34,34);"><br/></span>', '').replace('<p><font color="#222222"><br/></font></p>', '').replace('<br/><br/>', '<br/>').replace('<p><font><font></font><br/></font><br/></p>', '').replace('<p><span><br/></span><br/></p>', '').replace('<p><span style="color:rgb(255,0,0);font-size:16px;"><br/></span></p>', '').replace('<p><span style="font-size:12pt;"><br/></span></p>', '').replace('<p><font style="background-color:rgb(255,255,0);"><br/></font><br/></p>', '').replace('<p><span style="font-size:20px;"><br/></span><br/></p>', '').replace('<p style="background-color:rgb(252,253,253);"><span style="background-color:rgb(255,255,255);"><br/></span></p>', '').replace('<br/><span style="background-color:rgb(255,253,247);"> </span><br/>', '').replace('<p><span style="font-weight:700;"><br/></span></p>', '').replace('<p><span style="color:rgb(0,0,255);font-weight:700;"><br/></span></p>', '')

            space_free_html = " ".join(bad_string_free_html.split())
            f.seek(0)
            f.write(space_free_html)
            f.truncate()
        print(
            f"===========\nRemove Redundant String \"{filename}\" Complete.\n===========")


quick_generator('/home/eric/文件/json_soup', '/home/eric/文件/html_combined_soup')
RemoveRedundantTag('/home/eric/文件/html_combined_soup')
# RemoveRedundantString('/home/eric/文件/html_combined_soup')
