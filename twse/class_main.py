from browser import chrome
from bs4 import BeautifulSoup
from db import mysql
import time

# 證券編碼查詢
class Class_Main_Service:
    __url_stock = 'https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y'
    __url_etf = 'https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=I&industry_code=&Page=1&chklike=Y'

    __db = None
    __sql = "INSERT IGNORE INTO `twsd`.`stock`(`stock_code`, `stock_name`)VALUES(%s, %s)"


    def __init__(self):
        self.__db = mysql.TWSD_DB()
        self.__db.connect()
    

    def collection_stock_code(self):
        print("start collecting stock code")

        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()

        try:
            # 證券編碼
            cb.Browser.get(self.__url_stock)

            # wait
            time.sleep(2)

            # 解析
            soup = BeautifulSoup(cb.Browser.page_source, "lxml")
            tbody = soup.find("tbody")
            trs = tbody.find_all("tr")
            sql_val = list()
            for tr in trs[1:]:
                td = tr.find_all("td")
                assert len(td) == 10, 'Unrecognized database format!!!'
                row = (td[2].text, td[3].text)
                sql_val.append(row)

            # insert
            if len(sql_val) > 0:
                self.__db.executemany(self.__sql, sql_val)
        except Exception as e:
            print(e)
        finally:
            cb.Browser.close()
            print("stop collecting stock code")
    

    def collection_etf_code(self):
        print("start collecting etf code")

        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()

        try:
            # 證券編碼
            cb.Browser.get(self.__url_etf)

            # wait
            time.sleep(2)

            # 解析
            soup = BeautifulSoup(cb.Browser.page_source, "lxml")
            tbody = soup.find("tbody")
            trs = tbody.find_all("tr")
            sql_val = list()
            for tr in trs[1:]:
                td = tr.find_all("td")
                assert len(td) == 10, 'Unrecognized database format!!!'
                row = (td[2].text, td[3].text)
                sql_val.append(row)

            # insert
            if len(sql_val) > 0:
                self.__db.executemany(self.__sql, sql_val)
        except Exception as e:
            print(e)
        finally:
            cb.Browser.close()
            print("stop collecting etf code")