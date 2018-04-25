import win32com.client
from selenium import webdriver
from time import sleep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import sys
ie = win32com.client.Dispatch("InternetExplorer.Application")
ie.Visible = 1
ie.Navigate('https://find.ruten.com.tw/s/?q=sony')

while(True) :
    state = ie.ReadyState
    if (state == 4):
        
        break
    sleep(1)
print (ie.Document.body.innerHTML)
ie.Quit()
sys.exit()