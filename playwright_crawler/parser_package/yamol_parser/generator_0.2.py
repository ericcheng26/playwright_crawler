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
    b64data = base64.b64encode(raw).decode()
    return '<img src="data:image/jpeg;base64, ' + b64data + '>'


def img_to_base64(img_path):
    with open(img_path, 'rb') as f:
        raw = f.read()
    b64data = base64.b64encode(raw).decode()
    return '<img src="data:image/jpeg;base64, ' + b64data + '">'


def q_part_generator(q_list):
    result = '''    <table class="main_block">
    <tr>
      <td class="q_and_c">'''
    result += q_list[0]

    for c in q_list[1]:
        result += ('<br>' + c)
    result += '<table>'
    try:
        for img_path in q_list[3]:
            image = img_to_base64(img_path)
            result += ('<td class="q_image">' + image + '</td>')
    except IndexError:
        pass
    except TypeError:
        print('TypeError--Something going wrong!FIX ME!')
    except:
        print(img_path, '--Something going wrong!FIX ME!')

    result += '</table></td>'

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

    title = basename(single_json_path).replace('_note.json', '')
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
# 生成html內head和body
    result = '''\
    <title>我是標題</title>
    <style>
    body {
      margin: 0;
      padding: 0;
      background-color: gray;
      font-family: arial,"Microsoft JhengHei","微軟正黑體",sans-serif !important;
    }

    div{
      background-color: #fff !important;
    }

    div.block{
      margin: auto;
      background-color: #f7f7e6;
      width: 21.5cm;
      padding: 0.8cm;
    }

    h1.d_number {
      display: inline-block;
      font-family: serif;
      font-style: italic;
      font-size: 13pt;
      border-radius: 18px;
      background-color: LightGray;
      padding: 0.1cm;
      margin-block-start: 0em;
      margin-block-end: 0.1em;
      margin-inline-start: 0px;
      margin-inline-end: 0px;
    }

    h1.main_head{
      display: block;
      background-color: cyan;
      padding: 0.2cm;
      border-style: double;
      border-width: 0.25cm;
      text-align: center;
      font-weight: bold;
    }

    table.contents{
      border: 1px solid black;
      }

    a.head_contents{
      font-size:13px;
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
      margin: 0.3cm 0 0 0;
      border-bottom: 5px double black;
      padding:0cm;
    }
    p{
      display: block;
      margin-block-start: auto;
      margin-block-end: 5px;
      margin-inline-start: 0px;
      margin-inline-end: 0px;
      word-wrap: break-word;
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
      font-size: 13pt;
      text-align-last: center;
    }

    h2.qid{
      border-radius: 18px;
      background-color: LightGray;
      margin: 0cm 0 0.1cm 0;
      text-align-last: center;
      font-size: 13pt;
    }

    .alert {
      display: table;
      table-layout: fixed;
      width: 100%;
      font-family: serif;
      font-size: 12pt;
      word-wrap: break-word;
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
    td.q_image {
      border: hidden;
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
      word-wrap: break-word;
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

    a{
      word-wrap: break-word;
    }

    @media print{
      @page{
      widows:2;
      orphans:4;
      }

      header, nav, footer, video, audio, object, embed{
        display: none !important;
      }

      body{
        -webkit-print-color-adjust: economy;
        background-color: #fff !important;
        color: #000000;
        width: 100%;
        margin: 0;
        float: none;
        line-height: 1.3;
        font-size: 12pt;
        font-family:serif;
        padding-top: 68px;
        padding-bottom: 68px;
      }

      span{
        color: #000000 !important;
      }


      a.head_contents{
        display:none;
      }

      td.inner_contents{
        display:none;
      }
      td.q_and_c{
        background-color: #fff;
      }

      h2.qid{
        display:none;
      }

      div{
        background-color: #fff !important;
        -webkit-box-decoration-break: clone;
      }
      div.block{
        background-color: #fff;
      }

      table.ans_block{
        border: 1px solid;
        border-color: #000000;
        border-radius: 20px;
      }

      h1.main_head{
        background-color: LightGray !important;
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
        -webkit-box-decoration-break: clone;
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
# 生成html內目錄
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
# 生成題目、詳解討論和筆記
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
                '<p style="color:rgb(34,34,34);"><br/></p>', '').replace('<p><font color="#3152a9"><span style="background-color:rgb(255,255,255);font-size:11.7px;"><br/></span></font></p>', '').replace('<p><span style="color:rgb(34,34,34);"><br/></span></p>', '').replace('<p><spastyle><br/><br/></spastyle></p>', '').replace('<p><font><br/></font></p>', '').replace('<p><span style="font-size:20px;"><br/></span></p>', '').replace('<p style="color:rgb(68,68,68);"><br/></p>', '').replace('<p><span style="color:rgb(68,68,68);"><br/></span></p>', '').replace('<p><span style="font-size:1.1em;"><br/></span></p>', '').replace('<p><span style="color:rgb(51,51,51);font-size:14pt;"><br/></span></p>', '').replace('<span style="font-size:1.1em;"><br/></span>', '').replace('<span style="font-size:16.94px;"><br/></span>', '').replace('<p><b><span style="font-size:14px;"><br/></span></b></p>', '').replace('<p style="font-size:12pt;"> </p>', '').replace('<p><span style="font-size:15.4px;"><br/></span></p>', '').replace('<p><span style="font-size:15.4px;"><br/></span><br/></p>', '').replace('<p><span style="font-size:15.6px;"><br/></span><br/></p>', '').replace('<div><br/></div>', '').replace('<p><span style="color:rgb(17,17,17);"><br/></span></p>', '').replace('<span><br/></span>', '').replace('<p> <br/></p>', '').replace('<h4><br/></h4>', '').replace('<p style="color:rgb(0,0,0);"><br/></p>', '').replace('<p><br/><br/><br/></p>', '').replace("<p><span style=\"font-family:'微軟正黑體';\"><br/></span><br/></p>", '').replace("<p style=\"font-family:'微軟正黑體';font-size:12pt;\"><span style=\"font-weight:bold;color:rgb(91,155,213);\"><br/></span></p>", '').replace('<p><span style="color:rgb(85,85,85);"><br/></span></p>', '').replace('<p><br/></p>', '').replace('<p><span style="color:rgb(80,78,78);"><br/></span></p>', '').replace('<p><span style="color:rgb(80,78,78);background-color:rgb(247,247,247);"><br/></span><br/></p>', '').replace('<span style="color:rgb(34,34,34);"><br/></span>', '').replace('<p><font color="#222222"><br/></font></p>', '').replace('<br/><br/>', '<br/>').replace('<p><font><font></font><br/></font><br/></p>', '').replace('<p><span><br/></span><br/></p>', '').replace('<p><span style="color:rgb(255,0,0);font-size:16px;"><br/></span></p>', '').replace('<p><span style="font-size:12pt;"><br/></span></p>', '').replace('<p><font style="background-color:rgb(255,255,0);"><br/></font><br/></p>', '').replace('<p><span style="font-size:20px;"><br/></span><br/></p>', '').replace('<p style="background-color:rgb(252,253,253);"><span style="background-color:rgb(255,255,255);"><br/></span></p>', '').replace('<br/><span style="background-color:rgb(255,253,247);"> </span><br/>', '').replace('<p><span style="font-weight:700;"><br/></span></p>', '').replace('<p><span style="color:rgb(0,0,255);font-weight:700;"><br/></span></p>', '').replace('<p><font color="#222222"><b><br/></b></font><br/></p>', '').replace('<div class="6-2" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">6-2</h1> <div style="text-align:right"><i></i></div></div>', '').replace('<div class="13-2" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">13-2</h1> <p>題目錯誤</p> <div style="text-align:right"><i></i></div></div>', '').replace('<div class="13-3" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">13-3</h1> 原本題目:13.鐵在血中的運送,主要必須依靠由何種器官合成之何種分子結台? (A)由肝臟合成的4球蛋白之運鐵蛋白 (B)由肝臟合成的隊蛋白之運鐵蛋白 (C)由脾臟合成的球蛋白之運鐵蛋白 (D)由脾臟合成的球蛋白之運鐵蛋白 .修改成為<p>13.鐵在血中的運送,主要必須依靠由何種器官合成之何種分子結台? (A)由肝臟合成的α球蛋白之運鐵蛋白 (B)由肝臟合成的β蛋白之運鐵蛋白 (C)由脾臟合成的α球蛋白之運鐵蛋白 (D)由脾臟合成的β球蛋白之運鐵蛋白 .</p> <div style="text-align:right"><i></i></div></div>', '').replace('<span style="background-color:rgb(206,231,247);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(206,222,231);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(214,214,231);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(0,255,255);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(214,239,214);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(74,123,140);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(67,109,134);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(228,246,246);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(255,156,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(255,231,206);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(255,239,198);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(252,248,227);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(247,198,206);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(231,214,222);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(0,0,255);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(0,255,0);', '<span style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(255,255,0);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(0,0,255);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(231,214,222);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(247,198,206);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(252,248,227);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(255,239,198);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(255,231,206);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(255,156,0);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(228,246,246);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(67,109,134);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(214,239,214);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(0,255,255);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(214,214,231);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(206,222,231);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(206,231,247);', '<b style="background-color:#bdbdbd94;').replace('<b style="background-color:rgb(0,255,0);', '<b style="background-color:#bdbdbd94;').replace('<span style="color:rgb(255,255,255);background-color:rgb(74,123,140);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:20px;background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<i style="color:rgb(34,34,34);background-color:rgb(255,255,0);', '<i style="background-color:#bdbdbd94;').replace('<b style="color:rgb(34,34,34);font-family:sans-serif;background-color:rgb(255,255,0);', '<b style="background-color:#bdbdbd94;').replace('<u style="background-color:rgb(0,255,0);', '<u style="background-color:#bdbdbd94;').replace('<span style="font-weight:700;background-color:rgb(255,231,206);', '<span style="background-color:#bdbdbd94;').replace('如下：有核細胞總數＞5×109', '如下：有核細胞總數＞5×10<sup>9</sup>').replace('<span style="font-size:14px;background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-weight:700;background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:15.4px;background-color:rgb(255,255,0);', '<b style="background-color:#bdbdbd94;').replace('</span></h6>', '</span></h4>').replace('<h6><span>', '<h4><span>').replace('stain）<br/>(A)<br/>(B)<br/>(C)<br/>(D)<table>', 'stain）<table><tbody><tr><td>(A)</td><td>(B)</td><td>(C)</td><td>(D)</td></tr></tbody></table><table><tbody><tr><td>').replace('/JZo3/AFP/AGqb+dBBBTVfxO/W8n/Y38mf/9k="></td></tr></tbody></table>', '/JZo3/AFP/AGqb+dBBBTVfxO/W8n/Y38mf/9k="></td></tr></tbody></table></td></tr></tbody></table>').replace('<span style="font-family:Calibri;font-size:12pt;color:rgb(255,255,0);background-color:rgb(0,0,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(51,51,51);background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<i style="background-color:rgb(255,255,0);', '<i style="background-color:#bdbdbd94;').replace('<span style="background:rgb(204,255,204);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-weight:bold;background:rgb(204,255,255);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:11pt;background:rgb(255,255,153);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:11pt;font-weight:bold;background:rgb(255,255,153);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:#bdbdbd94;color:rgb(255,0,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(255,0,0);background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:12pt;background-color:rgb(255,255,0);color:rgb(255,0,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:12pt;background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(231,156,156);', '<span style="background-color:#bdbdbd94;').replace('<b style="color:rgb(0,0,0);font-size:14px;background-color:rgb(255,255,0);', '<b style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(255,255,119);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(64,64,64);background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(203,231,206);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-weight:700;color:rgb(34,34,34);background-color:rgb(252,248,227);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(34,34,34);background-color:rgb(252,248,227);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(34,34,34);background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(10,10,11);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(156,0,255);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:10.5pt;background:rgb(247,198,206);', '<span style="background-color:#bdbdbd94;').replace('<li><span style="color:rgb(1,1,1);"></span></li>', '').replace('<span style="font-weight:bold;background:#F2DCDB;', '<span style="background-color:#bdbdbd94;').replace('<span style="font-weight:bold;background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="background:#FFFF99;', '<span style="background-color:#bdbdbd94;').replace('<td style="background-color:#FADBD2;', '<td style="background-color:#fff;').replace('<div><h2>點開看表格</h2><table border="1"><tbody><tr><td style="background-color:#D0CECE;"></td></tr></tbody></table></div>', '').replace('<div><table border="1"><tbody><tr><td style="background-color:#D0CECE;"></td></tr></tbody></table></div>', '').replace('<span style="font-weight:bold;background:#FFFF99;', '<span style="background-color:#bdbdbd94;').replace('<font style="background-color:rgb(203,231,206);', '<font style="background-color:#bdbdbd94;').replace('<span style="color:rgb(192,152,83);background-color:rgb(252,248,227);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:16px;color:rgb(234,67,53);', '<span style="background-color:#bdbdbd94;').replace('<div class="76-1" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">76-1</h1> 答案 C <div style="text-align:right"><i></i></div></div>', '').replace('<div class="76-2" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">76-2</h1> 答案錯誤 c <div style="text-align:right"><i></i></div></div>', '').replace('<div class="76-3" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">76-3</h1> 原本答案為B,修改為C <div style="text-align:right"><i></i></div></div>', '').replace('<div class="77-2" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">77-2</h1> 答案 C <div style="text-align:right"><i></i></div></div>', '').replace('<div class="77-3" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">77-3</h1> 原本答案為D,修改為C <div style="text-align:right"><i></i></div></div>', '').replace('<div class="77-4" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">77-4</h1> 原本題目:77.下列何者是鼠痘（mousepox）的病原？ (A)Mouse vaccinia virus (B)Mouse cytomegalovirus (C)Ectromelia virus (D)Molluscipoxvirus 修改成為77.下列何者是鼠痘（mousepox）的病原？ (A)Mouse vaccinia virus (B)Mouse cytomegalovirus (C)Ectromelia virus (D)Molluscipoxvirus <div style="text-align:right"><i></i></div></div>', '').replace('<div class="78-1" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">78-1</h1> 答案 B <div style="text-align:right"><i></i></div></div>', '').replace('<div class="78-2" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">78-2</h1> <span style="background-color:rgb(245,245,245);">答案 B</span> <div style="text-align:right"><i></i></div></div>', '').replace('<div class="78-3" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">78-3</h1> 原本答案為C,修改為B <div style="text-align:right"><i></i></div></div>', '').replace('<div class="78-4" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">78-4</h1> 原本題目:78.下列何者可引起長尾鸚鵡鱗屑腳（scaly leg）？ (A)Cnemidocoptes mutans (B)Cnemidocoptes pilae (C)Dermanyssus gallinae (D)Echidnophaga gallinacean 修改成為78.下列何者可引起長尾鸚鵡鱗屑腳（scaly leg）？ (A)Cnemidocoptes mutans (B)Cnemidocoptes pilae (C)Dermanyssus gallinae (D)Echidnophaga gallinacean <div style="text-align:right"><i></i></div></div>', '').replace('<div class="78-5" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">78-5</h1> <p>一種蟎類', '<div class="78-1" style="table-layout: fixed; width: -webkit-fill-available; border: 1px solid; border-radius: 40px; border-color: #000000; padding: 8px 8px 11px 20px; margin-top: 7px; background-color:AliceBlue; font-size: 12pt; page-break-inside:avoid; -webkit-box-decoration-break: clone; "><h1 class="d_number">78-1</h1> <p>一種蟎類').replace('<span style="background-color:rgb(255,0,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(142,116,66);background-color:rgb(255,253,229);', '<span style="background-color:#bdbdbd94;').replace('<span style="background:#00FF00;', '<span style="background-color:#bdbdbd94;').replace('<span style="color:#00B050;', '<span style="background-color:#bdbdbd94;').replace('<span style="color:#FF0000;', '<span style="background-color:#bdbdbd94;').replace('<span style="background:#FFFF00;', '<span style="background-color:#bdbdbd94;').replace('<font style="background-color:rgb(255,255,0);', '<font style="background-color:#bdbdbd94;').replace('<span style="color:rgb(0,0,0);background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(221,75,57);background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(255,255,255);background-color:rgb(64,128,255);', '<span style="background-color:#bdbdbd94;').replace('<span style="background-color:rgb(255,253,229);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:inherit;background-color:rgb(255,255,0);', '<span style="background-color:#bdbdbd94;').replace('<span style="color:rgb(78,126,172);background-color:rgb(180,215,255);', '<span style="background-color:#bdbdbd94;').replace('<span style="font-size:1.8em;background-color:rgb(255,198,156);', '<span style="background-color:#bdbdbd94;')

            bad_string_free_html = bad_string_free_html.replace(
                '<br/>(', '@*@*').replace('<br/>', '').replace('@*@*', '<br/>(')
            space_free_html = " ".join(bad_string_free_html.split())
            f.seek(0)
            f.write(space_free_html)
            f.truncate()
        # print(
        #     f"===========\nRemove Redundant String \"{filename}\" Complete.\n===========")


quick_generator('/home/eric/文件/json_soup', '/home/eric/文件/html_combined_soup')
# 移除多餘的字串
RemoveRedundantTag('/home/eric/文件/html_combined_soup')
print('RemoveRedundantString Starting ！')
for i in range(1, 5):
    print(f'RemoveRedundantString 第{i}次！')
    RemoveRedundantString('/home/eric/文件/html_combined_soup')
print('RemoveRedundantString Complete ！')
