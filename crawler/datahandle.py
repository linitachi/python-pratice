# -*- coding: utf8 -*-
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from selenium import webdriver
import sys
import re

def WriteInExcel(filename, data,cellphone):
    with open(filename, 'a',newline='') as csv_file: #寫入不會有空行newline=''
        writer = csv.writer(csv_file)
        for i in range(len(data)):
            writer.writerow(cellphone[i])
            for j in range(len(data[i])):
                try:
                    writer.writerow([data[i][j]])
                except Exception: #因為無法解決編碼問題，因此把有特殊字元的狀況 丟出例外。
                    data[i][j]=data[i][j].encode("utf8")
                    data[i][j]=data[i][j].decode("cp950", "ignore")
                    writer.writerow([data[i][j]])
    return 1
newdata=[]
i=0 #控制excel行數
j=0 #控制手機型號
f=open("test.csv",'r')
data=f.readlines()
cellphone=["xzp",'xz1','xz','z5','z5p','xz2','other']
e=[1,2,4]
for k in range (len(cellphone)):
    newdata.append([])
while(1):
    if(re.search(cellphone[j], data[i],re.I)!=None):
        newdata[j].append(data[i])
        i+=1
        j=0
    else:
        j+=1
        if(j==len(cellphone)-1):
            newdata[j].append(data[i])
            i+=1
            j=0
    print(i)
    if(i==len(data)):
        break
print(newdata)
WriteInExcel('final.csv',newdata,cellphone)
