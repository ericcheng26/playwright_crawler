# path: <dir_patth>/<file_name>.json
# static_dir_path: <dir_path>/<static_dir>
# discussion_path: <dir_path>/<static_dir>/discussion.html

'''
========================
      使用方法
========================
1. 建立物件
  parser = Vet_yamol_parser(yamol_raw_html_string, path)

2. 執行分析並回傳路徑
  result_path = parser()
------------------------
  
quick parse in a dir: 

              quick_yamol_parser(html_dir, parsed_dir)
  
------------------------
  
========================
    關於檔案路徑
========================
分析的過程會把資料存下來
分成 json, 圖檔, discussion.html
後兩者會放在 static 的資料夾
------------------------
'''

from os.path import isabs, isfile, isdir, basename, dirname, join
from os import makedirs, listdir
from json import load, dump
from bs4 import BeautifulSoup as BS
import requests
import re


class Vet_yamol_parser():
    # 初始化，用於存取 raw data 與 建立 DOM
    def __init__(self, html, path):
        self.html = html
        self.path = path

        self.dom = BS(html, 'lxml')
        self.domlist = self.dom.select('[class="col-lg-12 reponse-card"]')

        self.static_dir = join(dirname(path), 'static')

        self.discussion_path = join(self.static_dir, 'discussion.html')

        self.note_path = join(self.static_dir, 'note.html')

        # 建立 json 檔的佔存容器
        self.container = {}

    # 萃取所求資料，並序列化

    def __call__(self):
        # domlist loop
        for bstag in self.domlist:

            # 取得題目與選項
            qid, question, choices = self._get_choice_question(bstag)

            # 取得答案
            try:
                ans = self._get_ans(bstag)
            except:
                print(f'分析第{qid}題時發生問題')

            # 儲存圖片並回傳路徑
            img_path_list = self._img_extract(bstag, qid, self.static_dir)

            # 儲存詳解討論
            try:
                self._extract_discussion(bstag, qid, self.discussion_path)
            except:
                print(f'分析第{qid}題討論時發生問題')

            # 儲存私人筆記
            self._extract_note(bstag, qid, self.note_path)

            # 打包成字典
            result = self._todict(qid, question, choices, ans, img_path_list)

            self.container.update(result)

        self.result_path = self._serialize(self.container, self.path)
        return self.result_path

#############################以下為內部方法的實作##########################################

    def _get_choice_question(self, bstag):
        itemcontent = bstag.select('[class="itemcontent"]')
        text = itemcontent[0].getText().replace('\n', ' ')

        if '重新載圖' in text:
            question, temp_choices = text[text.find(
                '重新載圖')+4:text.find('(A)')].strip(), text[text.find('(A)'):].strip()
        else:
            question, temp_choices = text[:text.find(
                '(A)')].strip(), text[text.find('(A)'):].strip()

        choices = []
        for c in ['(B)', '(C)', '(D)']:
            i = temp_choices.find(c)
            choices.append(temp_choices[:i].strip())
            temp_choices = temp_choices[i:]
        choices.append(temp_choices)
        qid_re = re.search(r'(\d+)\s*[.]', question)
        # print(qid_re.group(1))
        qid = qid_re.group(1)

        # 若 choices 全空，則代表選項全是圖片
        if not all(choices):
            re_pattern_choice = r'\(A\) <span(.*)<span></span></span>'
            re_pattern_img = r'(<img src=.*?/>)'
            raw_choice = re.search(re_pattern_choice, str(
                itemcontent[0]), re.DOTALL).group(1)
            choices = re.findall(re_pattern_img, raw_choice, re.DOTALL)

        return qid, question, choices

    def _get_ans(self, bstag):
        answer = bstag.select('[class="col-sm-6 col-md-4 col-lg-4"]')
        text = answer[0].getText()
        ans = text[text.find('答案：')+3]
        return ans

    def _img_save(self, url, path):

        if (not isdir(dirname(path))) and (dirname(path) != ''):
            makedirs(dirname(path))

        response = requests.get(url)
        file = open(path, "wb")
        file.write(response.content)
        file.close()
        return path

    def _img_extract(self, bstag, qid, static_path):
        content = bstag.select('[class="itemcontent"]')
        imglist = content[0].select('img')
        if imglist == []:
            return None
        else:
            img_path_list = []
            for i, img in enumerate(imglist):
                img_src = img['src']
                path = join(static_path, qid + '_' + str(i) + '.jpg')
                img_path = self._img_save(img_src, path)
                img_path_list.append(img_path)
            return img_path_list

    def _todict(self, number, question, choices, answer, image_path=None, solution=None, ):

        if isinstance(number, int) or isinstance(number, float):
            number = str(int(number))

        # print(number)
        #print(re.search(r'(\d+)[.]', question))
        if number != re.search(r'(\d+)\s?[.]', question).group(1):
            raise ValueError('Wrong question number!')

        if len(choices) != 4:
            try:
                raise Warning(f'There are {len(choices)} choice(s), not 4!')
            except Warning as w:
                print('Warning: %s' % w)

        if not any([answer in choice[:3] for choice in choices]):
            print('='*15)
            print('出現例外')
            print('-'*15)
            print('題目:', number)
            print('原始選項:', choices)
            print('答案:', answer)
            try:
                raise ValueError('No such answer!')
            except ValueError as e:
                print(e)
                if 'e' in answer.lower():
                    choices.append(choices[3][choices[3].find('(E)'):])
                    choices[3] = choices[3][:choices[3].find('(E)')]
                    print('修改後選項: ', choices)
                print('='*15)

        result = {number: [question, choices, answer]}

        if image_path != None:
            result[number].append(image_path)
        return result

    def _serialize(self, container: dict, path: str):

        if not isinstance(container, dict):
            raise TypeError('The 1st arg. must be a dictionary.')

        if isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = load(f)
        else:
            if (not isdir(dirname(path))) and (dirname(path) != ''):
                makedirs(dirname(path))
            data = {}

        data.update(container)

        with open(path, 'w', encoding='utf-8') as f:
            dump(data, f, ensure_ascii=False)
        if dirname(path) != '':
            print(f'已建立 {basename(path)} 於 {dirname(path)}')
            return [basename(path), dirname(path)]
        else:
            print(f'已建立 {path} 於當前工作資料夾')
            return path

    def _extract_discussion(self, bstag, qid, doc_path):
        if (not isdir(dirname(doc_path))) and (dirname(doc_path) != ''):
            makedirs(dirname(doc_path))

        img_size_control = r'''
        <style type="text/css">
          img{max-width:80%; height: auto;}
        </style>
    '''
        re_pattern = r'<span class="comment">(.*)<a href="support_open.php\?extra_type'
        addition_filter = r'<label class="badge badge-danger">已解鎖</label>'
        addition_filter2 = r'style="display:none"'
        re_pattern2 = r'查看完整內容</a></div>(.*div style="text-align:right"><i>)'
        div_open = r'<div style="border: 2px solid red; border-radius: 5px; border-color: gray; padding: 25px 25px 25px 25px; margin-top: 25px;" class=<class>>'
        if str(qid) == '61':
            print(bstag)
        discussion_list = bstag.select(
            '[class="well itemcomment"] div[style*="min-height"]')

        with open(doc_path, 'a', encoding='utf-8') as f:
            f.write(img_size_control)

        if str(qid) == '61':
            print(discussion_list)
        for i, e in enumerate(discussion_list):
            if '查看完整' in str(e):
                re_result = re.search(re_pattern2, str(e), re.DOTALL)
                target = re_result.group(1).replace(addition_filter2, '')
            else:
                if str(qid) == '61':
                    print(str(e))
                re_result = re.search(re_pattern, str(e), re.DOTALL)
                target = re_result.group(1).replace(addition_filter, '')

            result = div_open + f'<h1>{qid}-{i+1}</h1>' + target + '</div>'*2

            with open(doc_path, 'a', encoding='utf-8') as f:
                f.write(result)

    def _extract_note(self, bstag, qid, doc_path):

        img_size_control = r'''
        <style type="text/css">
          img{max-width:80%; height: auto;}
        </style>
    '''
        css_selector = r'li[class*="list-group-item well itemcomment"]'
        re_pattern = r'已解鎖</label><br/>(.*)\n<center>'
        div_open = r'<div style="border: 2px solid red; border-radius: 5px; border-color: gray; padding: 25px 25px 25px 25px; margin-top: 25px;" class=<class>>'

        note_list = bstag.select(css_selector)

        if not note_list:
            return None

        with open(doc_path, 'a', encoding='utf-8') as f:
            f.write(img_size_control)

        for i, e in enumerate(note_list):
            try:
                re_result = re.search(re_pattern, str(e), re.DOTALL)
                target = re_result.group(1)
                result = div_open.replace('<class>', str(
                    qid) + '-' + str(i+1)) + f'<h1>{qid}-{i+1}</h1>' + target + '</div>'*2
            except:
                print(f'分析 note 第 {str(qid)}-{str(i+1)} 出問題')

            with open(doc_path, 'a', encoding='utf-8') as f:
                f.write(result)

    def _extract_discussion(self, bstag, qid, doc_path):
        if (not isdir(dirname(doc_path))) and (dirname(doc_path) != ''):
            makedirs(dirname(doc_path))

        img_size_control = r'''
        <style type="text/css">
          img{max-width:80%; height: auto;}
        </style>
    '''
        re_pattern = r'<span class="comment">(.*)<a href="support_open.php\?extra_type'
        addition_filter = r'<label class="badge badge-danger">已解鎖</label>'
        addition_filter2 = r'style="display:none"'
        re_pattern2 = r'查看完整內容</a></div>(.*div style="text-align:right"><i>)'
        div_open = r'<div style="border: 2px solid red; border-radius: 5px; border-color: gray; padding: 25px 25px 25px 25px; margin-top: 25px;" class=<class>>'

        discussion_list = bstag.select(
            '[class="well itemcomment"] div[style*="min-height"]')

        with open(doc_path, 'a', encoding='UTF-8') as f:
            f.write(img_size_control)

        for i, e in enumerate(discussion_list):
            if '查看完整' in str(e):
                re_result = re.search(re_pattern2, str(e), re.DOTALL)
                target = re_result.group(1).replace(addition_filter2, '')
            else:
                re_result = re.search(re_pattern, str(e), re.DOTALL)
                target = re_result.group(1).replace(addition_filter, '')

            result = div_open.replace('<class>', str(
                qid) + '-' + str(i+1)) + f'<h1>{qid}-{i+1}</h1>' + target + '</div>'*2

            with open(doc_path, 'a', encoding='UTF-8') as f:
                f.write(result)


def quick_yamol_parser(html_dir, parsed_dir):
    # 取出所有 html 檔，轉成 .json
    parsed_path_list = [
        join(
            join(parsed_dir,
                 basename(p).replace('.html', '')
                 ),
            basename(p).replace('.html', '.json')
        )
        for p in listdir(html_dir) if '.html' in basename(p)
    ]

    html_path_list = [join(html_dir, p)
                      for p in listdir(html_dir) if 'html' in basename(p)]

    # print(html_path_list)
    # print(parsed_path_list)

    # rp == raw path
    for rp, pp in zip(html_path_list, parsed_path_list):
        with open(rp, 'rb') as f:
            print(f'開始分析 {basename(rp)}')
            Vet_yamol_parser(f.read().decode('utf-8'), pp)()
