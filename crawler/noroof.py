# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from selenium import webdriver
import sys
data = []
# chromedriver.exe執行檔所存在的路徑
chrome_path = "C:\selenium_driver_chrome\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

driver.get("https://find.ruten.com.tw/c/002100010003?sort=new%2Fdc")
html = driver.page_source
# driver.close()
soup = BeautifulSoup(html, 'html.parser')
name = []
price = []

for name_box in soup.find_all('h5', 'prod_name'):  # 找出商品名
    name.append(name_box.text)

for price_box in soup.find_all('span', attrs={'class': 'price'}):  # 找出價格
    if(price_box.text != ''):
        price.append(price_box.text)

# print(len(price), len(name)) 因為有廣告所以價格比商品名多

for i in range(len(name)):
    print(name[i], '價格為:', price[i])
