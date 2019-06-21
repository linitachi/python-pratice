from selenium import webdriver
import time

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import csv


class Pchome():
    def __init__(self):
        self.chrome_path = "./chromedriver_win32/chromedriver.exe"
        self.driver = webdriver.Chrome(self.chrome_path)
        # self.driver.get(
        #     "https://24h.pchome.com.tw/prod/DSAB04-A9008GEKP")
        self.driver.get(
            "https://ecshweb.pchome.com.tw/search/v3.3/?q=%E7%98%8B%E6%AE%BA%E7%89%B9%E8%B3%A3"
        )

    def Search(self):
        self.driver.find_element_by_id("keyword").send_keys("瘋殺特賣")
        self.driver.find_element_by_id("doSearch").click()

    def Product(self):
        for i in range(1, 30):
            # 滾動頁面，讓全部商品顯現
            self.driver.execute_script(
                "window.scrollTo(0,document.body.scrollHeight);")
        for link in self.driver.find_elements_by_xpath(
                '//*[@class="prod_name"]/a'):
            # print(link.get_attribute('href')) #印出商品網址
            print("商品名稱:", link.text)
            item_driver = webdriver.Chrome(self.chrome_path)
            item_driver.get(link.get_attribute('href'))
            time.sleep(1)
            Buy, price, Spread = self.Decisionprice(item_driver)
            print("是否要購買:", Buy)
            if Buy:
                WriteInExcel("nice.csv", link.text, link.get_attribute('href'),
                             price, Spread)
                # a = self.driver.find_elements_by_class_name("prod_name")

    def Decisionprice(self, item_driver):
        while 1:
            Slogan = item_driver.find_element_by_id("SloganContainer").text
            index = Slogan.find("網路價")
            if index != -1:
                string = "網路價"
                break
            index = Slogan.find("原價$")
            if index != -1:
                string = "原價$"
                break
            item_driver.quit()
            return False, 0, 0

        if string == "網路價":
            originprice = self.getPrice(Slogan, Slogan.find("網路價") + 4)
            currentprice = self.getPrice(Slogan, Slogan.find("限時價") + 5)
        elif string == "原價$":
            originprice = self.getPrice(Slogan, Slogan.find("原價$") + 3)
            currentprice = self.getPrice(Slogan, Slogan.find("好物推薦價") + 6)
        print("originprice:", originprice)
        print("currentprice:", currentprice)
        # 想買的價格
        item_driver.quit()
        if originprice - currentprice >= 1000 and originprice < 4000:
            return True, currentprice, originprice - currentprice
        if originprice - currentprice > 3000:
            return True, currentprice, originprice - currentprice
        return False, 0, 0

    def getPrice(self, str, pos):
        tem = []
        price = 0
        for i in range(len(str)):
            # 判斷是否為數字 如果不是直接跳出 ex:網路價$13900． 限時價↘$7988
            try:
                tem.append(float(str[pos + i]))
            except ValueError:
                break
        for i in range(len(tem)):
            price = price + tem[-1 - i] * (10**i)
        return price


def WriteInExcel(filename, name, URL, price, Spread):
    with open(filename, 'a', newline='') as csv_file:  # 寫入不會有空行newline=''
        writer = csv.writer(csv_file)
        writer.writerow([name, URL, price, Spread])


if __name__ == '__main__':
    pch = Pchome()
    # pch.Search()
    pch.Product()
    # pch.Decisionprice()
    pch.driver.quit()
