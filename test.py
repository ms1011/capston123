import pandas as pd
from bs4 import BeautifulSoup
import MySQLdb
from sqlalchemy import create_engine
import pymysql
import requests
import pprint
from wordcloud import WordCloud
from konlpy.tag import Komoran      # 형태소 분석기


db_connection_str = 'mysql+pymysql://crawl_usr:Test001@localhost/crawl_data'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()

# 주식갤러리 주소
url = 'https://gall.dcinside.com/board/lists/?id=neostock'
# &page=1

# 전체 페이지 읽어오기
df = pd.DataFrame()

for page in range(1, int(50)+1):
    page_url = '{}&page={}'.format(url, page)
    response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(response_page)[0])

df = df.dropna()            # 쓰레기값 제거
df = df.drop_duplicates()   # 중복제거

df['단어'] = df['제목'].str.split(' ')
# print(type(df['단어']))       # <class 'pandas.core.series.Series'>
# print(type(df1))             # <class 'pandas.core.frame.DataFrame'>

pp = pprint.PrettyPrinter(indent=4)

komoran = Komoran()
wordCounts = {}
for word in df['단어']:
    # words.append(word)
    for i in word:
        if i not in wordCounts:
            wordCounts[i] = 0
        wordCounts[i] += 1
# pp.pprint(wordCounts)

# 단어 구름 만들기
wc = WordCloud(
    font_path='NanumGothic.ttf',
    background_color='white',
)
wcImg = wc.generate_from_frequencies(wordCounts)
wcImg.to_file('wordcloud.jpg')

# df.to_sql(name='crawl_data', con=db_connection, if_exists='append', index=False)


# 한페이지에 있는 모든 게시글을 가져온다
# with requests.get(url, headers={'User-agent': 'Mozilla/5.0'}) as doc:
#     soup = BeautifulSoup(doc.content, 'html.parser')
#     contents = soup.find('tbody').find_all('tr')
#
#     for i in contents:
#         # 글 번호 추출
#         numTag = i.find('td', class_='gall_num')
#         num = numTag.text
#         if (num == '공지' or num == '설문') == False:
#             print("글번호: ", num)
#             # 제목 추출
#             title = i.find('a').text
#             print("제목: ", title)
#             print("="*20)
