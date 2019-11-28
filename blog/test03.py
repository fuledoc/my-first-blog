#from textblob import Textblob
import requests
from bs4 import BeautifulSoup
from sys import argv

class Analysis:
    def __init__(self, term):
        self.term = term
        self.subjectivity = 0
        self.sentiment = 0

        #self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.term)
        self.url = 'https://www.google.com/search?q={0}&source=lnms'.format(self.term)
        #print(self.url)
    def run(self):
        response = requests.get(self.url)
        #print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        #headline_results = soup.find_all('div', class_='st')
        #headline_results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd') # 내용
        headline_results = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd') # 제목
        #headline_results = soup.find_all('span', class_='r0bn4c rQMQod') # 일자

        #print(soup)
        #print(headline_results)
        for h in headline_results:
            print(h)
            #blob = TextBlob(h.get_text())
            #self.sentiment += blob.sentiment.polarity / len(headline_results)
            #self.subjectivity += blob.sentiment.subjectivity / len(headline_results)


            #print(h)

#a = Analysis(argv[1])
a = Analysis('질의어 본 고안은 탄성 있게 등받이를 지지하여 주는 틸팅유닛과, 이를 구비한 의자와 관련되며, 실시예로 좌판과 등받이를 이어주며, 등받이의 탄성')
a.run()

#print(a.term, 'Subjectivity: ', a.subjectivity, 'Sentiment: ', a.sentiment)
