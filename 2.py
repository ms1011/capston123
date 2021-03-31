import pandas as pd
from bs4 import BeautifulSoup
import requests
from matplotlib import pyplot as plt
import mplfinance as mpf

# 네이버에서 크롤링 막아놓음

# 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.nhn?code=051910&page=1'
with requests.get(url, headers={'User-agent': 'Mozilla/5.0'}) as doc:
    html = BeautifulSoup(doc.text, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]
    print(last_page)

# 전체 페이지 읽어오기
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=051910'

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)
    response_page = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(response_page)[0])

df = df.dropna()
print(df)

# # 차트 출력을 위해 데이터프레임 가공
# df = df.dropna()
# df = df.reset_index(drop=True)  # index reset
# print(df)
#
# # 30일간 종가 추이 확인
# df = df.iloc[0:30]
# df = df.sort_values(by='날짜')
#
# # 날짜, 종가 칼럼으로 차트 그리기
# plt.title('Lg Chemical (close)')
# plt.xticks(rotation=45)
# plt.plot(df['날짜'], df['종가'], 'co-')
# plt.grid(color='gray', linestyle='--')
# plt.show()
#
# # 캔들차트 작성
# df = df.rename(columns={'날짜': 'Date', '시가': 'Open', '고가': 'High', '저가': 'Low', '종가': 'Close', '거래량': 'Volume'})
# df = df.sort_values(by='Date')
# df.index = pd.to_datetime(df.Date)
# df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
#
# kwargs = dict(title='LG Chemical Candle Chart', type='candle', mav=(10,20,30), volume=True, ylabel='ohic candles')
# # mav : moving average
# mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
# s = mpf.make_mpf_style(marketcolors=mc)
# mpf.plot(df, **kwargs, style=s)