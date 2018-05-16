# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from selenium import webdriver
import sys


def current_page_info(soup):
    name = []
    price = []
    for name_box in soup.find_all('h5', 'prod_name'):  # 找出商品名
        name.append(name_box.text)

    for price_box in soup.find_all('span', attrs={'class': 'price'}):  # 找出價格
        if(price_box.text != ''):
            price.append(price_box.text)
        # print(len(price), len(name)) 因為有廣告所以價格比商品名多

    #for i in range(len(name)):
        #print(name[i], '價格為:', price[i])
       
    return name, price


def WriteInExcel(filename, name, price):
    with open(filename, 'a',newline='') as csv_file: #寫入不會有空行newline=''
        writer = csv.writer(csv_file)
        for i in range(len(name)):
            #name[i]=name[i].encode("utf8")
            #name[i]=name[i].decode("cp950", "ignore")
            try:
                writer.writerow([name[i], price[i]])
            except Exception: #因為無法解決編碼問題，因此把有特殊字元的狀況 丟出例外。
                name[i]=name[i].encode("utf8")
                name[i]=name[i].decode("cp950", "ignore")
                writer.writerow([name[i], price[i]])
    return 1


# chromedriver.exe執行檔所存在的路徑
chrome_path = "C:\selenium_driver_chrome\chromedriver.exe"

driver = webdriver.Chrome(chrome_path)

url = 'https://find.ruten.com.tw/c/002100010003?sort=new%2Fdc'

times = 1  # 跑幾個頁面
page = 2  # 代表第幾頁

for i in range(times):
    # 開啟網頁
    driver.get(url)
    # 讀取當頁面的html
    html = driver.page_source
    # 分析當前頁面的資訊
    soup = BeautifulSoup(html, 'html.parser')
    name, price = current_page_info(soup)
    WriteInExcel('test.csv', name, price)
    # 找出下一頁的網址
    url = 'https://find.ruten.com.tw/c/002100010003?p=' + \
        str(page)+'&sort=new%2Fdc'
    page += 1

#driver.close()
