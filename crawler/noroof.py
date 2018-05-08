# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from selenium import webdriver
import sys
data = []
# quote_page = 'https://www.google.com.tw/search?q=%E4%BD%A0%E5%A5%BD&oq=%E4%BD%A0%E5%A5%BD&aqs=chrome..69i57j0l5.12793j0j8&sourceid=chrome&ie=UTF-8'
# chromedriver.exe執行檔所存在的路徑
chrome_path = "C:\selenium_driver_chrome\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

driver.get("https://find.ruten.com.tw/c/002100010003")
html = driver.page_source
driver.close()
soup = BeautifulSoup(html, 'html.parser')
name = []
price = []
for name_box in soup.find_all('h5'):
    name.append(name_box.text)
for price_box in soup.find_all('span'):
    price.append(price_box.text)
for i in range(len(name)):
    print(name[i], price[i])
'''req = Request('',
              headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req).read()
# page = urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
data = []
# for name_box in soup.find('h3', attrs={'class': 'r'}).parent.find_all('h3'):
for name_box in soup.find_all('h3'):
    print(name_box.text)
'''
sys.exit()
