from bs4 import BeautifulSoup as BS
import ssl, urllib
import traceback

base_url = 'https://www.google.co.kr/search'
target = '자전거'
#: 검색조건 설정
values = {
    'q': target, # 검색할 내용
    'oq': target,
    'aqs': 'chrome..69i57.35694j0j7',
    'sourceid': 'chrome',
    'ie': 'UTF-8',
}

# Google에서는 Header 설정 필요
hdr = {'User-Agent': 'Mozilla/5.0'}

query_string = urllib.parse.urlencode(values)
req = urllib.request.Request(base_url + '?' + query_string, headers=hdr)
context = ssl._create_unverified_context()

try:
    res = urllib.request.urlopen(req, context=context)
except:
    traceback.print_exc()

html_data = BS(res.read(), 'html.parser')

g_list = html_data.find_all('div', attrs={'class': 'g'})

try:
    for g in g_list:
        # 컨텐츠 URL 꺼내기
        ahref = g.find('a')['href']
        ahref = 'https://www.google.co.kr' + ahref

        # 컨텐츠에서 검색결과와 일치하는 부분 꺼내기
        span = g.find('span', attrs = {'class': 'st'})
        if span:
            span_text = span.get_text()
            span_text = span_text.replace(' ', '')
            span_text = span_text.replace('\n', '')
except:
    traceback.print_exc()


print(g_list)
