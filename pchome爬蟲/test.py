from selenium import webdriver
import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


class Pchome():
    def __init__(self):
        self.chrome_path = "./chromedriver_win32/chromedriver.exe"
        self.driver = webdriver.Chrome(self.chrome_path)
        # self.driver.get(
        #     "https://24h.pchome.com.tw/prod/DSAB04-A9008GEKP")
        self.driver.get(
            "https://ecshweb.pchome.com.tw/search/v3.3/?q=%E7%98%8B%E6%AE%BA%E7%89%B9%E8%B3%A3")

    def Search(self):
        self.driver.find_element_by_id("keyword").send_keys("瘋殺特賣")
        self.driver.find_element_by_id("doSearch").click()

    def Product(self):
        for i in range(1, 30):
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);")
        for link in self.driver.find_elements_by_xpath('//*[@class="prod_name"]/a'):
            print(link.get_attribute('href'))
            print(link.text)
            self.driver.get(link.get_attribute('href'))
            Buy = self.Decisionprice()
            if Buy:
                # 寫入excel
            print("===========")
        # a = self.driver.find_elements_by_class_name("prod_name")

    def Decisionprice(self):
        while 1:
            Slogan = self.driver.find_element_by_id("SloganContainer").text
            index = Slogan.find("網路價")
            if index != -1:
                string = "網路價"
                break
            index = Slogan.find("原價$")
            if index != -1:
                string = "原價$"
                break
        if string == "網路價":
            originprice = self.getoriginalPrice(Slogan, Slogan.find("網路價")+4)
            currentprice = self.getCurrentPrice(Slogan, Slogan.find("限時價")+5)
        elif string == "原價$":
            originprice = self.getoriginalPrice(Slogan, Slogan.find("原價$")+3)
            currentprice = self.getCurrentPrice(Slogan, Slogan.find("好物推薦價")+6)
        print(originprice)
        print(currentprice)
        # 想買的價格
        if originprice-currentprice >= 1000 and originprice < 4000:
            return True
        if originprice-currentprice > 3000:
            return True
        return False

    def getoriginalPrice(self, str, pos):
        tem = []
        price = 0
        for i in range(len(str)):
            # 判斷是否為數字 如果不是直接跳出 ex:網路價$13900． 限時價↘$7988
            try:
                tem.append(float(str[pos+i]))
            except ValueError:
                break
        for i in range(len(tem)):
            price = price + tem[-1-i] * (10 ** i)
        return price

    def getCurrentPrice(self, str, pos):
        tem = []
        price = 0
        for i in range(len(str)):
            # 判斷是否為數字 如果不是直接跳出 ex:網路價$13900． 限時價↘$7988
            try:
                tem.append(float(str[pos+i]))
            except ValueError:
                break
        for i in range(len(tem)):
            price = price + tem[-1-i] * (10 ** i)
        return price


if __name__ == '__main__':
    pch = Pchome()
    # pch.Search()
    pch.Product()
    # pch.Decisionprice()
    pch.driver.quit()
