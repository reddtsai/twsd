from browser import chrome
from bs4 import BeautifulSoup
from db import mysql
from selenium.webdriver.support.ui import Select
import time

# 個股日成交資訊
class Stock_Day_Service:
    __url = 'https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html'

    __db = None
    __sql = """REPLACE INTO `twsd`.`quote`
    (`stock_code`, `quote_date`, `opening_price`, `closing_price`, `highest_price`, `lowest_price`)
    VALUES(%s, %s, %s, %s, %s, %s)"""


    def __init__(self):
        self.__db = mysql.TWSD_DB()
        self.__db.connect()
    

    def collection(self, stock_code, trans_yyyy, trans_mm):
        print("start collecting stock price", stock_code, trans_yyyy, trans_mm)

        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()

        try:
            # 個股日成交
            cb.Browser.get(self.__url)

            # wait
            time.sleep(1.5)

            # 資料日期
            select_all = Select(cb.Browser.find_element_by_name("yy"))
            select_all.select_by_value(trans_yyyy)
            select_all = Select(cb.Browser.find_element_by_name("mm"))
            select_all.select_by_value(trans_mm)
            # 股票代碼
            input_stock_code = cb.Browser.find_element_by_name("stockNo")
            input_stock_code.clear()
            input_stock_code.send_keys(stock_code)
            cb.Browser.find_element_by_xpath("//form").submit()
            # wait
            time.sleep(2)

            assert 'report-table' in cb.Browser.page_source, 'No data!!!'

            # 解析
            soup = BeautifulSoup(cb.Browser.page_source, "lxml")
            table = soup.find("table", {"id": "report-table"})
            tbody = table.find("tbody")
            trs = tbody.find_all("tr")
            sql_val = list()
            for tr in trs:
                td = tr.find_all("td")
                row = self.sql_val(stock_code, td)
                if row is not None:
                    sql_val.append(row)

            # insert
            if len(sql_val) > 0:
                self.__db.executemany(self.__sql, sql_val)

        except Exception as e:
            print(e)
        finally:
            cb.Browser.close()
            print("stop collecting stock price", stock_code, trans_yyyy, trans_mm)

    
    def collection_history(self, stock_code, from_yyyy, from_mm, to_yyyy, to_mm):
        print("start collecting stock price history", stock_code)

        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()

        try:
            # 個股日成交
            cb.Browser.get(self.__url)

            # wait
            time.sleep(1.5)

            assert '個股日成交資訊' in cb.Browser.page_source, 'Page is not ready!!!' 

            start_yyyy = from_yyyy
            end_yyyy = to_yyyy + 1
            for yyyy in range(start_yyyy, end_yyyy):
                start_mm = 1
                end_mm = 13
                if yyyy == from_yyyy and from_mm != 0:
                    start_mm = from_mm
                if yyyy == to_yyyy and to_mm != 0:
                    end_mm = to_mm + 1
                for mm in range(start_mm, end_mm):
                    print(yyyy, mm)

                    # 資料日期
                    select_all = Select(cb.Browser.find_element_by_name("yy"))
                    select_all.select_by_value(str(yyyy))
                    select_all = Select(cb.Browser.find_element_by_name("mm"))
                    select_all.select_by_value(str(mm))
                    # 股票代碼
                    input_stock_code = cb.Browser.find_element_by_name("stockNo")
                    input_stock_code.clear()
                    input_stock_code.send_keys(stock_code)
                    cb.Browser.find_element_by_xpath("//form").submit()
                    # wait
                    time.sleep(2)

                    assert 'report-table' in cb.Browser.page_source, 'No data!!!'

                    # 解析
                    soup = BeautifulSoup(cb.Browser.page_source, "lxml")
                    table = soup.find("table", {"id": "report-table"})
                    tbody = table.find("tbody")
                    trs = tbody.find_all("tr")
                    sql_val = list()
                    for tr in trs:
                        td = tr.find_all("td")
                        row = self.sql_val(stock_code, td)
                        if row is not None:
                            sql_val.append(row)

                    # insert
                    if len(sql_val) > 0:
                        self.__db.executemany(self.__sql, sql_val)

                    time.sleep(2)

        except Exception as e:
            print(e)
        finally:
            cb.Browser.close()
            print("stop collecting stock price", stock_code)


    def sql_val(self, stock_code, td):
        row = None
        td_len = len(td)
        assert td_len == 9, 'Unrecognized database format!!!'

        try:
            # 日期
            dd = td[0].text.split('/')
            yyyy = int(dd[0]) + 1911
            quote_date = str(yyyy) + dd[1] + dd[2]

            # 開盤價
            td3 = td[3].text.replace(',', '')
            opening_price = float(td3)

            # 收盤價
            td6 = td[6].text.replace(',', '')
            closing_price = float(td6)

            # 最高價
            td4 = td[4].text.replace(',', '')
            highest_price = float(td4)

            # 最低價
            td5 = td[5].text.replace(',', '')
            lowest_price = float(td5)
            

            row = (stock_code, quote_date, opening_price, closing_price, highest_price, lowest_price)
        except Exception as e:
            raise e

        return row