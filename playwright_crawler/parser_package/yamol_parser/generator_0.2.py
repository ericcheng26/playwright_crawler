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
        result += '<h2>詳解</h2>\n'

        for tag in d_tag_list:
            result += str(tag)

    if n_tag_list != None and n_tag_list != []:
        result += '<h2>筆記</h2>'

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

    result = '''\
    <style>
    body {
      margin: 0;
      padding: 0;
      background-color: gray;
    }
    
    div.block{
      margin: auto;
      background-color: white;
      width: 21cm;
      padding: 1cm;
    }
    
    h1.main_head{
      background-color: cyan;
      padding: 0.5cm;
      border-style: double;
      border-width: 0.25cm;
      text-align: center;
      font-weight: bold;
      font-family: DFKai-sb;
    }
    
    table.contents{
      border: 1px solid black;
      }
    
    a.head_contents{
      font-size:0.7cm;
      padding:0.3cm;
      border-radius: 5px;
      background-color:LightGray;
    }
    
    thead{height:2cm;}
    
    td.inner_contents{
      border: 1.5px solid black;
      width: 1cm;
      background-color: LightYellow;
      text-align: center;
    }
    
    div.q_block{
      margin: 2cm 0 0 0;
      border-top: 5px solid black;
      border-bottom: 5px double black;
      padding:0cm;
    }
    
    h2.qid{
      border-radius: 5px;
      background-color:LightGray;
      padding:0.5cm;
      margin:0.1cm 0 0.2cm 0;
    }
    .alert {
      border: 1px solid rgb(232 232 232);
      border-top-color: rgb(232, 232, 232);
      border-top-style: solid;
      border-top-width: 1px;
      border-right-color: rgb(232, 232, 232);
      border-right-style: solid;
      border-right-width: 1px;
      border-bottom-color: rgb(232, 232, 232);
      border-bottom-style: solid;
      border-bottom-width: 1px;
      border-left-color: rgb(232, 232, 232);
      border-left-style: solid;
      border-left-width: 1px;
      border-image-source: initial;
      border-image-slice: initial;
      border-image-width: initial;
      border-image-outset: initial;
      border-image-repeat: initial;
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
      border-radius: 5px;
      width:100%;
      background-color: LightYellow;
      margin:0.1cm 0 0.3cm 0;
    }
    td {
      border-collapse:collapse;
      border-top: 1px solid #a9a9a9;
      border-top-width: 1px;
      border-top-style: solid;
      border-top-color: rgb(165 165 165);
    }
    tr{
      border-collapse: collapse;
      border-top: 1px solid #a9a9a9;
      border-top-width: 1px;
      border-top-style: solid;
      border-top-color: rgb(165 165 165)
    }
    img {
      min-width: -webkit-fill-available;
      max-width: -webkit-fill-available;
      max-height: fit-content;
    }
    
    table.ans_block{
      border-radius: 5px;
      background-color:LightGray;
      margin:0.1cm 0 0.3cm 0;
      width:100%;
    }
    
    td.ans_head{
      padding:0.2cm;
      font-weight: bold;
      font-family: DFKai-sb;
      border:hidden;
    }
    
    td.ans_val{
      padding:0.2cm;
      text-align: right;
      border:hidden;
    }
    
    div.note_and_discussion{
      border-radius: 5px;
      background-color:AliceBlue;
      width:100%;
      margin-bottom: 0.5cm;
    }
    
    *{
    word-break: break-all;
    }
    
    @media print{
    
      body{
        background-color: white;
      }
      h1.main_head{
        background-color: white;
        padding: 15cm 0 0 0;
        border-style: none;
        height: 17cm;
      }
    }
  </style>
  
  <body>

  <div class=block>

  <h1 class=main_head>
    我是標題
  </h1>
  
  <div style="margin:0 0 0.5cm 0;"><a name=contents class=head_contents>目錄</a></div>
    <table class=contents >
    <tr>\
  '''.replace('我是標題', title)

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
    return result, title


# 把str儲存成html檔
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


quick_generator('/home/eric/文件/json_soup', '/home/eric/文件/html_combined_soup')
