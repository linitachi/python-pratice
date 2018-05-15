import requests
import time
from bs4 import BeautifulSoup
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
import sys
import os
import json

PTT_URL = 'https://www.ptt.cc'


def get_web_page(url):
    time.sleep(1)  # 每次爬取前暫停 0.5 秒以免被 PTT 網站判定為大量惡意爬取
    resp = requests.get(
        url=url,
        cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')

    # 取得上一頁的連結
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']

    articles = []  # 儲存取得的文章資料
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').string.strip() == date:  # 發文日期正確
            # 取得推文數
            push_count = 0
            if d.find('div', 'nrec').string:
                try:
                    push_count = int(d.find('div', 'nrec').string)  # 轉換字串為數字
                except ValueError:  # 若轉換失敗，不做任何事，push_count 保持為 0
                    pass
            # 取得文章連結及標題
            if d.find('a'):  # 有超連結，表示文章存在，未被刪除
                author = d.find('div', 'author').string
                href = d.find('a')['href']
                title = d.find('a').string
                articles.append({
                    'title': title,
                    'href': href,
                    'push_count': push_count,
                    'author': author
                })
    return articles, prev_url


def parse(dom):
    soup = BeautifulSoup(dom, 'html.parser')
    links = soup.find(id='main-content').find_all('a')
    img_urls = []
    for link in links:
        if re.match(r'^https?://(i.)?(m.)?imgur.com', link['href']):
            img_urls.append(link['href'])
    return img_urls


def save(img_urls, title):
    if img_urls:
        try:
            dname = title.strip()  # 用 strip() 去除字串前後的空白
            os.makedirs(dname)
            for img_url in img_urls:
                if img_url.split('//')[1].startswith('m.'):
                    img_url = img_url.replace('//m.', '//i.')
                if not img_url.split('//')[1].startswith('i.'):
                    img_url = img_url.split(
                        '//')[0] + '//i.' + img_url.split('//')[1]
                if not img_url.endswith('.jpg'):
                    img_url += '.jpg'
                fname = img_url.split('/')[-1]
                urllib.request.urlretrieve(img_url, os.path.join(dname, fname))
        except Exception as e:
            print(e)


def Content_data(url, Keywords):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    main_content = soup.find(id="main-content")
    metas = main_content.select('div.article-metaline')
    filtered = [v for v in main_content.stripped_strings if v[0]
                not in [u'※', u'◆'] and v[:2] not in [u'--']]
    content = ' '.join(filtered)
    content = re.sub(r'(\s)+', '', content)
    contentt = main_content.text

    number_start = contentt.find(u'欲售價格' or u'交易價格')
    number_end = contentt.find(u'\n', number_start)

    try:
        author = metas[0].select('span.article-meta-value')[0].string
        title = metas[1].select('span.article-meta-value')[0].string
    except IndexError as n:
        author = '??'
        title = '??'
    if(title[1] != '賣'):  # 如果不是賣 就返回0
        return 0
    if(re.findall(Keywords, title.lower()) == []):  # 如果找不到關鍵字 就返回0
        return 0
    date = metas[2].select('span.article-meta-value')[0].string
    price = contentt[number_start+5:number_end]

    data = [[author, date, title.lower(), price]]
# 這裡要注意一下存的格()  []
    with open('index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['標題', '價格', '發文日期', '作者', '爬的時間'])
        for author, date, title, price in data:
            writer.writerow([title, price, date, author, datetime.now()])
    return 1


def Content_data22(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, "html.parser")
    main_content = soup.find(id="main-content")
    metas = main_content.select('div.article-metaline')
    filtered = [v for v in main_content.stripped_strings if v[0]
                not in [u'※', u'◆'] and v[:2] not in [u'--']]
    content = ' '.join(filtered)
    content = re.sub(r'(\s)+', '', content)
    contentt = main_content.text

    number_start = contentt.find(u'欲售價格' or u'交易價格')
    number_end = contentt.find(u'\n', number_start)
    try:
        author = metas[0].select('span.article-meta-value')[0].string
        title = metas[1].select('span.article-meta-value')[0].string
    except IndexError as n:
        author = '??'
        title = '??'
    if(title[1] != '賣'):  # 如果不是賣 就返回0
        return 0
    date = metas[2].select('span.article-meta-value')[0].string
    price = contentt[number_start+5:number_end]
    data = [[author, date, title.lower(), price]]
# 這裡要注意一下存的格()  []
    if(price != ''):
        data = [[author, date, title.lower(), price]]
    else:
        return 0
    with open('index.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['標題', '價格', '發文日期', '作者', '爬的時間'])
        for author, date, title, price in data:
            writer.writerow([title, price, date, author, datetime.now()])
        return 1


if __name__ == '__main__':
    current_page = get_web_page(
        'https://www.ptt.cc/bbs/mobilesales/index.html')
    if current_page:
        articles = []  # 全部的今日文章
        # 今天日期, 去掉開頭的 '0' 以符合 PTT 網站格式
        date = time.strftime("%m/%d").lstrip('0')
        current_articles, prev_url = get_articles(
            current_page, date)  # 目前頁面的今日文章

        while current_articles:  # 若目前頁面有今日文章則加入 articles，並回到上一頁繼續尋找是否有今日文章
            articles += current_articles
            current_page = get_web_page(PTT_URL + prev_url)
            current_articles, prev_url = get_articles(current_page, date)
        for article in articles:
            page = get_web_page(PTT_URL + article['href'])
            if page:
                print(PTT_URL + article['href'])
                Content_data(PTT_URL + article['href'], 'sony')
            #Content_data(page, 'sony')
            print('done')
        # 已取得文章列表，開始進入各文章讀圖
        '''for article in articles:
            print('Processing', article)
            page = get_web_page(PTT_URL + article['href'])
            if page:
                soup = BeautifulSoup(page, 'html.parser')
                content=soup.find('div',attrs={'id':'main-content'})
                k=0
                str1=''
                for j in range(len(content.text)):
                    if(content[j]=='欲'or content[j]=='物' or k==1):
                        k=1
                        str1+=content[j]
                    if(content[j]=='※'):
                        break
                print(str1)
                with open('index.csv', 'a') as csv_file:
                    writer=csv.writer(csv_file)
                    writer.writerow([str1, datetime.now()])
        '''
