# APIを利用してパーマリンクを収集するには機関としてAPI利用を申請する必要がある。
# 面倒なのでスクレイピングで行い、csvにパーマリンクを一覧で保存する。
import requests
from bs4 import BeautifulSoup
import csv

# リサーチマップをcurlで取得
url = f"https://researchmap.jp/researchers"
institute = "東京大学"
url_for_search = url + "?q=" + institute
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
data = requests.get(url_for_search, headers=headers).text

# Webページの情報からパーマリンクを取得
soup = BeautifulSoup(data, 'html.parser')
cards = soup.find_all('div', class_='rm-cv-card-outer')
permalinks = []
for card in cards:
    a_tag = card.find('a', href=True)
    if a_tag:
        href_value = a_tag['href'].lstrip('/')
        permalinks.append(href_value)
        print(href_value)

# パーマリンクをcsvに保存
with open('permalinks.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Permalink'])
    for permalink in permalinks:
        writer.writerow([permalink])