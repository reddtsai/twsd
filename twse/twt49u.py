from browser import chrome
from bs4 import BeautifulSoup
from db import mysql
from selenium.webdriver.support.ui import Select
import time

# 除權除息
class TWT49_Service:

    def __init__(self):
        self.__url_twt49 = 'https://www.twse.com.tw/zh/page/trading/exchange/TWT49U.html'
        self.__url_t108sb19 = 'https://mops.twse.com.tw/mops/web/t108sb19_q1'
        self.__db = mysql.TWSD_DB()
        self.__db.connect()
        
    def get(self, from_year, from_month, from_date, to_year, to_month, to_date):
        print("start twt49u", from_year, to_year)
        
        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()

        try:
            # 除權除息計算結果表
            cb.Browser.get(self.__url_twt49)
            time.sleep(2)
            # 資料日期
            select_from_year = Select(cb.Browser.find_element_by_xpath("//div[@id='d1']/select[@name='yy']"))
            select_from_year.select_by_value(from_year)
            select_from_month = Select(cb.Browser.find_element_by_xpath("//div[@id='d1']/select[@name='mm']"))
            select_from_month.select_by_value(from_month)
            select_from_date = Select(cb.Browser.find_element_by_xpath("//div[@id='d1']/select[@name='dd']"))
            select_from_date.select_by_value(from_date)
            select_to_year = Select(cb.Browser.find_element_by_xpath("//div[@id='d2']/select[@name='yy']"))
            select_to_year.select_by_value(to_year)
            select_to_month = Select(cb.Browser.find_element_by_xpath("//div[@id='d2']/select[@name='mm']"))
            select_to_month.select_by_value(to_month)
            select_to_date = Select(cb.Browser.find_element_by_xpath("//div[@id='d2']/select[@name='dd']"))
            select_to_date.select_by_value(to_date)
            cb.Browser.find_element_by_xpath("//form").submit()

            # wait
            time.sleep(5)

            # 全部
            select_all = Select(cb.Browser.find_element_by_name("report-table_length"))
            select_all.select_by_value("-1")
            
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
                self.__db.dividend_executemany("REPLACE INTO `twsd`.`dividend`(`stock_code`,`stock_name`,`dividend_date`,`declare_data`,`dividend_year`,`dividend_month`,`dividend_day`,`dividend`,`dividend_type`,`dividend_status`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", sql_val)
        except Exception as e:
            print(e)
        finally:
            cb.Browser.close()
            print("stop twt49u", from_year, to_year)
        
    def sql_val(self, td):
        row = None
        td_len = len(td)
        if td_len not in [15, 17]:
            return row
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
            # declare_date = self.get_dividend_declare_date(stock_code, yyy[0])

            # 除權息
            dividend = None
            # 除權息類型
            dividend_type = 0
            if td_len == 15:
                if td[5].text != '':
                    td5 = td[5].text.replace(',', '')
                    dividend = float(td5)
                
                txt6 = td[6].text
                if txt6 == '息':
                    dividend_type = 2
                elif txt6 == '權':
                    dividend_type = 1
                elif txt6 == '權息':
                    dividend_type = 3
            elif td_len == 17:
                if td[7].text != '':
                    td7 = td[7].text.replace(',', '')
                    dividend = float(td7)
                
                txt8 = td[8].text
                if txt8 == '息':
                    dividend_type = 2
                elif txt8 == '權':
                    dividend_type = 1
                elif txt8 == '權息':
                    dividend_type = 3
                
            # 除權息狀態
            dividend_status = 1

            row = (stock_code, stock_name, dividend_date, declare_date, dividend_year, dividend_month, dividend_day, dividend, dividend_type, dividend_status)
        except Exception as e:
            raise e

        return row

    def get_dividend_declare_date(self, stock_code, yyy):
        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()
        declare_date = ''
        try:
            cb.Browser.get(self.__url_t108sb19)
            # 歷史資料
            select_is_new = Select(cb.Browser.find_element_by_id("isnew"))
            select_is_new.select_by_value('false')
            # 公司代號
            input_stock_code = cb.Browser.find_element_by_id("co_id")
            input_stock_code.clear()
            input_stock_code.send_keys(stock_code)
            # 年度
            input_stock_year = cb.Browser.find_element_by_id("YEAR")
            input_stock_year.clear()
            input_stock_year.send_keys(yyy)
            # 查詢
            div_search_bar1 = cb.Browser.find_elements_by_xpath("//div[@id='search_bar1']")[5]
            input_bnt = div_search_bar1.find_elements_by_xpath("div/input")[0]
            input_bnt.click()

            # wait
            time.sleep(1)

            soup = BeautifulSoup(cb.Browser.page_source, "lxml")
            form = soup.find("form", {"id": "t108sb22_fm1"})
            if form is not None:
                table = form.find("table")
                tr = table.find_all("tr")
                td = tr[1].find_all("td")
                declare_date = td[0].text
        except Exception as e:
            raise e
        finally:
            cb.Browser.close()

        return declare_date 
