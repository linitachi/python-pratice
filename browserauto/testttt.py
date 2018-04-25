import win32com.client
from selenium import webdriver
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
import sys

chrome_path = "C:\selenium_driver_chrome\chromedriver.exe" #chromedriver.exe執行檔所存在的路徑
driver = webdriver.Chrome(chrome_path)

driver.get('https://www.google.com/?hl=zh-tw')

driver.maximize_window()
driver.find_element_by_css_selector('a.gb_P').click()
