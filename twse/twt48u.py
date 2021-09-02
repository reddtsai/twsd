from browser import chrome
from bs4 import BeautifulSoup
from db import mysql
from selenium.webdriver.support.ui import Select
import time

# 除權除息預告
class TWT48_Service:
    __url = 'https://www.twse.com.tw/zh/page/trading/exchange/TWT48U.html'

    __db = None
    __sql = "REPLACE INTO `twsd`.`dividend`\
    (`stock_code`,`stock_name`, `dividend_date`, `declare_data`, `dividend_year`, `dividend_month`, `dividend_day`, `dividend`, `dividend_type`)\
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"


    def __init__(self):
        self.__db = mysql.TWSD_DB()
        self.__db.connect()


    def collection(self):
        print("start collecting twt48u")

        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()

        try:
            # 除權除息預告表
            cb.Browser.get(self.__url)

            # wait
            time.sleep(2)

            # 全部
            select_all = Select(cb.Browser.find_element_by_name("report-table_length"))
            select_all.select_by_value("-1")
            
            assert 'report-table_length' in cb.Browser.page_source, 'No data!!!'
            
            # 解析
            soup = BeautifulSoup(cb.Browser.page_source, "lxml")
            table = soup.find("table", {"id": "report-table"})
            tbody = table.find("tbody")
            trs = tbody.find_all("tr")
            sql_val = list()
            for tr in trs:
                td = tr.find_all("td")
                row = self.sql_val(td)
                if row is not None:
                    sql_val.append(row)

            # insert
            if len(sql_val) > 0:
                self.__db.executemany(self.__sql, sql_val)
        except Exception as e:
            print(e)
        finally:
            cb.Browser.close()
            print("stop collecting twt48u")


    def sql_val(self, td):
        row = None
        assert len(td) == 13, 'Unrecognized database format!!!'

        try:
            # 股票代號
            stock_code = td[1].text

            # 股票名稱
            stock_name = td[2].text

            # 除權除息日期-年
            d = td[0].text
            yyy = d.split('年')
            dividend_year = int(yyy[0]) + 1911

            # 除權除息日期-月
            mm = yyy[1].split('月')
            dividend_month = int(mm[0])

            # 除權除息日期-日
            dd = mm[1].split('日')
            dividend_day = int(dd[0])

            # 除權除息日期
            dividend_date = str(dividend_year) + mm[0] + dd[0]

            # 除權除息預告日期
            declare_date = ''
            # declare_date = get_dividend_declare_date(stock_code, yyy[0])

            # 除權息
            dividend = None
            if td[7].text != '':
                td7 = td[7].text.replace(',', '')
                dividend = float(td7)

            # 除權息類型
            dividend_type = 0
            td6 = td[6].text
            if td6 == '息':
                dividend_type = 2
            elif td6 == '權':
                dividend_type = 1
            elif td6 == '權息':
                dividend_type = 3

            row = (stock_code, stock_name, dividend_date, declare_date, dividend_year, dividend_month, dividend_day, dividend, dividend_type)
        except Exception as e:
            raise e

        return row