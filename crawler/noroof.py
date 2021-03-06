# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from selenium import webdriver
import sys
import re

def current_page_info(soup):
    name = []
    price = []
    SourcePage=[]#網址
    for name_box in soup.find_all('h5', 'prod_name'):  # 找出商品名
        name.append(name_box.text)
        SourcePage.append(name_box.find('a').get('href'))
    for price_box in soup.find_all('span', attrs={'class': 'price'}):  # 找出價格
        if(price_box.text != ''):
            price.append(price_box.text)
        # print(len(price), len(name)) 因為有廣告所以價格比商品名多

    #for i in range(len(name)):
        #print(name[i], '價格為:', price[i])
       
    return name, price,SourcePage


def WriteInExcel(filename, name, price,SourcePage,Addedtime):
    with open(filename, 'a',newline='') as csv_file: #寫入不會有空行newline=''
        writer = csv.writer(csv_file)
        for i in range(len(name)):
            try:
                Addedtime[i]=Addedtime[i].encode("utf8")
                Addedtime[i]=Addedtime[i].decode("cp950", "ignore")
                writer.writerow([name[i], price[i],SourcePage[i],Addedtime[i]])
            except Exception: #因為無法解決編碼問題，因此把有特殊字元的狀況 丟出例外。
                name[i]=name[i].encode("utf8")
                name[i]=name[i].decode("cp950", "ignore")
                Addedtime[i]=Addedtime[i].encode("utf8")
                Addedtime[i]=Addedtime[i].decode("cp950", "ignore")
                writer.writerow([name[i], price[i],SourcePage[i],Addedtime[i]])
    return 1

def WriteInExcel_noAddedtime(filename, name, price,SourcePage):
    with open(filename, 'a',newline='') as csv_file: #寫入不會有空行newline=''
        writer = csv.writer(csv_file)
        for i in range(len(name)):
            try:
                writer.writerow([name[i], price[i],SourcePage[i]])
            except Exception: #因為無法解決編碼問題，因此把有特殊字元的狀況 丟出例外。
                name[i]=name[i].encode("utf8")
                name[i]=name[i].decode("cp950", "ignore")
                writer.writerow([name[i], price[i],SourcePage[i]])
    return 1


def Added_time(SourcePage):#SourcePage:list
    time=[]
    for j in range(len(SourcePage)):
        driver.get(SourcePage[j])
         # 讀取當頁面的html
        html = driver.page_source
        # 分析當前頁面的資訊
        soup = BeautifulSoup(html, 'html.parser')
        time.append(soup.find('li','upload-time').text)
    return time

def SpecificItem(key,title,price,SourcePage): #只留下輸入的關鍵字
    j=0
    while(1):
        if(re.findall(key,title[j]) == []):
            del title[j]
            del price[j]
            del SourcePage[j]
            j-=1
        j+=1
        if(j==len(title)):
            break

# chromedriver.exe執行檔所存在的路徑
chrome_path = "C:\selenium_driver_chrome\chromedriver.exe"

driver = webdriver.Chrome(chrome_path)

url = 'https://find.ruten.com.tw/c/002100010003?sort=new%2Fdc'

times = 5  # 跑幾個頁面
page = 2  # 代表第幾頁 固定從2開始

for i in range(times):
    # 開啟網頁
    driver.get(url)
    # 讀取當頁面的html
    html = driver.page_source
    # 分析當前頁面的資訊
    soup = BeautifulSoup(html, 'html.parser')
    name, price,SourcePage = current_page_info(soup)

    SpecificItem('xzp',name, price,SourcePage)
    WriteInExcel_noAddedtime('test.csv', name, price,SourcePage)
    #WriteInExcel('test.csv', name, price,SourcePage,Added_time(SourcePage))
    # 找出下一頁的網址
    url = 'https://find.ruten.com.tw/c/002100010003?p=' + \
        str(page)+'&sort=new%2Fdc'
    print('第%s頁done 時間:%s'%(page-1,datetime.now() ) )
    page += 1
   

#driver.close()
