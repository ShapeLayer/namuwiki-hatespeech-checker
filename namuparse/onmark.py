'''
Imported from openNAMU


BSD 3-Clause License

Copyright (c) 2017-2021, surplus-dev
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import re
from datetime import datetime

class onmarkParse:
    def __init__(self, data: str):
        self.data = data
    
    def __str__(self):
        return self.data
    
    def processing(string: str) -> str:
        parsing: onmarkParse = onmarkParse(string)
        return parsing.remove_tags()

    def remove_tags(self):
        result = self.data
        result = self.remove_text_decoration(result)
        result = self.replace_braces(result)
        result = self.remove_link(result)
        result = self.replace_footnote(result)
        result = self.replace_macros(result)
        result = self.process_redirect(result)
        return result
    
    def remove_text_decoration(self, data: str) -> str:
        data = re.sub(r"'''((?:(?!''').)+)'''", r"\1", data)            # '''bold'''
        data = re.sub(r"''((?:(?!'').)+)''", r"\1", data)               # ''italic''
        data = re.sub(r"__((?:(?!__).)+)__", r"\1", data)               # __underline__
        data = re.sub(r"\^\^\^((?:(?!\^\^\^).)+)\^\^\^", r"\1", data)   # ^^^sup^^^
        data = re.sub(r"\^\^((?:(?!\^\^).)+)\^\^", r"\1", data)         # '''^^sup^^'''
        data = re.sub(r",,,((?:(?!,,,).)+),,,", r"\1", data)            # ,,,sub,,,
        data = re.sub(r",,((?:(?!,,).)+),,", r"\1", data)               # ,,sub,,
        data = re.sub(r"~~((?:(?!--).)+)~~", r"\1", data)               # ~~strikethrough~~
        data = re.sub(r"--((?:(?!--).)+)--", r"\1", data)               # --strikethrough--
        data = re.sub(r"={1,}#? (.*?) #?={1,}", r"\1", data)            # == paragraph title ==
        return data
    
    def replace_braces(self, data: str) -> str:
        data = re.sub(r"{{{\+[0-9]* (.*?)}}}", r"\1", data)             # 텍스트 크기
        data = re.sub(r"{{{#(.*?) (.*?)}}}", r"\2", data)               # 텍스트 색상
        # data = re.sub(r"{{{#!folding (.*).*}}}", r"\1", data, flags=re.MULTILINE)
        data = re.sub(r"{{{(.*?)}}}", r"\1", data)                      # literal (주의: 다른 {{{}}} 문법도 한번에 처리해버림)
        return data

    def remove_link(self, data: str) -> str:
        data = data.replace('../', '')
        data = re.sub(r"\[\[파일:(.*?)\]\]", r"", data)                  # [[파일:??]]
        data = re.sub(r"\[\[(.*?)\|(.*?)\]\]", r"\2", data)             # [[링크|표가]]
        data = re.sub(r"\[\[(.*?)\]\]", r"\1", data)                    # [[문서]] (fallback)
        return data

    def replace_footnote(self, data: str) -> str:
        data = re.sub(r"(\[(footnote|각주)\])", r"", data)
        footnotes: list = re.findall(r"(?:\[\*([^ \]]*)(?: ((?:(?!\]).)+))?\])", data)
        for result in footnotes:
            footnote_head: str = result[0] if result[0] else '*'
            data += f'{footnote_head} {result[1]}'
        data = re.sub(r"(?:\[\*([^ \]]*)(?: ((?:(?!\]).)+))?\])", r"", data)
        return data
    
    def replace_macros(self, data: str) -> str:
        data = data.replace('[date]', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data = data.replace('[datetime]', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        data = data.replace('[목차]', '')
        data = data.replace('[tableofcontents]', '')
        data = data.replace('[각주]', '')
        data = data.replace('[footnote]', '')
        data = data.replace('[br]', '\n')
        data = data.replace('[clearfix]', '')
        data = re.sub(r"\[include(\(.*?\))\]", r"", data)
        # data = re.sub(r"\[include(\(.*?\))\]", r"연결된 문서: \1", data)
        data = re.sub(r"\[pagecount(\(.*?\))?\]", r"", data)
        data = re.sub(r"\[(youtube|kakaotv|nicovideo|vimeo|navertv)\((.*?)\)\]", r" (동영상 링크) ", data)
        data = re.sub(r"\[ruby(\((.*?),.?ruby=(.*?)(,.*?)?\))\]", r"\2(\3)", data)

        # [age(YYYY-MM-DD)], [dday(YYYY-MM-DD)]
        for find in re.findall(r"\[(age|dday)\((.*?)\)\]", data):
            date: datetime = datetime.now()
            try:
                date = datetime.strptime(find[1], '%Y-%m-%d')
            except ValueError:
                continue
            now: datetime = datetime.now()
            res = 0
            if find[0] == 'age':
                res = now.year - date.year
                res += -1 if now.month < date.month or (now.month == date.month and now.day < date.day) else 0
            elif find[0] == 'dday':
                res = (now - date).days
            data = data.replace(f'[{find[0]}({find[1]})]', f'{res}')
        return data

    def process_redirect(self, data: str) -> str:
        return data
    
    def process_table(self, data: str) -> str:
        table_regex = {
            'total': re.compile(r"((?:(?:(?:(?:\|\|)+)|(?:\|[^|]+\|(?:\|\|)*))\n?(?:(?:(?!\|\|).)+))(?:(?:\|\||\|\|\n|(?:\|\|)+(?!\n)(?:(?:(?!\|\|).)+)\n*)*)\|\|)\n", re.MULTILINE),
            'cell': re.compile(r"((?:\|\|)+)((?:(?!\|\|).)*)", re.MULTILINE), # $1 = ||?, $2 = body
            'caption': re.compile(r"^\|([^|]+)\|", re.MULTILINE)
        }
        content = ''
        res = re.findall(table_regex['total'], data)
        for table in res:
            row = re.findall(table_regex['cell'], table)
            for partition, cell in row:
                content += cell
                print(cell)
        data = re.sub(table_regex['total'], content, data)
        return data

if __name__ == '__main__':
    #parsed: onmarkParse = onmarkParse("'''testhighlighter'''")
    #print(parsed.remove_tags())
    print(onmarkParse.process_table(None, open('../in.in', encoding='utf-8').read()))
