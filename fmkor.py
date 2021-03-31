import pandas as pd
from bs4 import BeautifulSoup
import MySQLdb
from sqlalchemy import create_engine
import pymysql
import requests

db_connection_str = 'mysql+pymysql://crawl_usr:Test001@localhost/fmkor_data'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()

# 주식갤러리 주소
url = 'https://www.fmkorea.com/index.php?mid=stock'
# &page=1

# 전체 페이지 읽어오기
df = pd.DataFrame()

for page in range(1, int(50)+1):
    page_url = '{}&page={}'.format(url, page)
    response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(response_page)[0])

df = df.dropna()
df = df.drop_duplicates()
print(df)

df.to_sql(name='fmkor_data', con=db_connection, if_exists='append', index=False)