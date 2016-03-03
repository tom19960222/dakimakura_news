import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import dateutil.parser
import datetime
import dateutil.tz
from pytz import timezone
import sys
import json

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

req = requests.get("http://www.nijigenshingu.info/makura/log/%s.html" % sys.argv[1])
req.encoding = 'euc-jp'
# print(strip_tags(req.text))

bs = BeautifulSoup(req.text, "html.parser")
img_list = bs.find_all('img')
striped_text = strip_tags(req.text).split('\n')
original_text = req.text.split('\n')
new_list = []
info_start_line = -1
simple_info_end_line = -1
dakimakura_list = []

for i in striped_text:
    if len(i) > 0:
        new_list.append(i)
for i in range(0, len(new_list)):
    # print(striped_text[i])
    if new_list[i].strip() == '【詳細情報】':
        # print("Data start at " + str(i))
        info_start_line = i
for i in range(0, len(original_text)):
    if original_text[i].strip().__contains__('【詳細情報】'):
        simple_info_end_line = i

simple_info_str = ''.join(req.text.split('\n')[0:simple_info_end_line])
bs_simple = BeautifulSoup(simple_info_str, "html.parser")
simple_info_list = bs_simple.find_all('td')

i = info_start_line+1
img_index = 0
simple_info_index = 3

content_template = """
<img src="%s" />
<p>
名称：%s <br />
メーカー： %s <br />
サイズ：%s <br />
価格：%s <br />
素材：%s <br />
発売日：%s <br />
販売：%s <br />
その他：%s <br />
</p>
"""

while i < len(new_list):
    tmpDaki = dict()
    tmpDaki['publish_date'] = new_list[i].replace('【', '').replace('】', '')
    tmpDaki['name'] = new_list[i+1].split('：')[1].strip()
    tmpDaki['maker'] = new_list[i+2].split('：')[1].strip()
    tmpDaki['size'] = new_list[i+3].split('：')[1].strip()
    tmpDaki['price'] = new_list[i+4].split('：')[1].strip()
    tmpDaki['material'] = new_list[i+5].split('：')[1].strip()
    tmpDaki['sale_date'] = new_list[i+6].split('：')[1].strip()
    tmpDaki['sale_by'] = new_list[i+7].split('：')[1].strip()
    tmpDaki['other'] = new_list[i+8].split('：')[1].strip()
    tmpDaki['image'] = img_list[img_index]['src']
    if simple_info_list[simple_info_index+1].a is not None:
        tmpDaki['link_item'] = simple_info_list[simple_info_index+1].a['href']
    tmpDaki['description'] = content_template % (tmpDaki['image'], tmpDaki['name'], tmpDaki['maker'], tmpDaki['size'], tmpDaki['price'], tmpDaki['material'], tmpDaki['sale_date'], tmpDaki['sale_by'], tmpDaki['other'])
    dakimakura_list.append(tmpDaki)
    i += 9
    img_index += 1
    simple_info_index += 3

dakimakura_list_JSON = json.dumps(dakimakura_list)
print(dakimakura_list_JSON)

# fg = FeedGenerator()
# fg.id('http://www.nijigenshingu.info/index2.shtml')
# fg.title('イ～☆えるの二次元★寝具情報')
# fg.link(href='http://www.nijigenshingu.info/index2.shtml')
# fg.language('jp')
# fg.description('イ～☆えるの二次元★寝具情報')

# for i in dakimakura_list:
#     fe = fg.add_entry()
#     fe.title(i['name'])
#     fe.published(timezone('Asia/Tokyo').localize(dateutil.parser.parse(i['publish_date'])))
#     fe.updated(datetime.datetime.now(timezone('Asia/Taipei')))
#     if 'link_item' in i:
#         fe.id(i['link_item'])
#         fe.link({'href': i['link_item']})
#     else:
#         fe.id(i['name'])
#     fe.description(content_template % (i['image'], i['name'], i['maker'], i['size'], i['price'], i['material'],
#                                    i['sale_date'], i['sale_by'], i['other']))
# print(fg.rss_str().decode('utf-8'))
# for i in bs.find_all('td'):
#     print(i)

# for i in bs.find_all('img'):
#     print(i['src'])
