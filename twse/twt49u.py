from bs4 import BeautifulSoup
from db import mysql
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

class TWT49_Service:
    def __init__(self):
        self._url = 'https://www.twse.com.tw/zh/page/trading/exchange/TWT49U.html'
        self._db = mysql.TWSD_DB()
        self._db.connect()
        
    def get(self, from_year, from_month, from_date, to_year, to_month, to_date):
        print("start twt49u")
        
        # Chrome Options
        option = webdriver.ChromeOptions()
        option.add_argument('--headless') 

        # Chrome
        browser  = webdriver.Chrome(executable_path='./drivers/chromedriver', options=option)

        try:
            # 除權除息計算結果表
            browser.get(self._url)
            # 資料日期
            select_from_year = Select(browser.find_element_by_xpath("//div[@id='d1']/select[@name='yy']"))
            select_from_year.select_by_value(from_year)
            select_from_month = Select(browser.find_element_by_xpath("//div[@id='d1']/select[@name='mm']"))
            select_from_month.select_by_value(from_month)
            select_from_date = Select(browser.find_element_by_xpath("//div[@id='d1']/select[@name='dd']"))
            select_from_date.select_by_value(from_date)
            select_to_year = Select(browser.find_element_by_xpath("//div[@id='d2']/select[@name='yy']"))
            select_to_year.select_by_value(to_year)
            select_to_month = Select(browser.find_element_by_xpath("//div[@id='d2']/select[@name='mm']"))
            select_to_month.select_by_value(to_month)
            select_to_date = Select(browser.find_element_by_xpath("//div[@id='d2']/select[@name='dd']"))
            select_to_date.select_by_value(to_date)
            browser.find_element_by_xpath("//form").submit()

            # wait
            time.sleep(6)

            # 全部
            select_all = Select(browser.find_element_by_name("report-table_length"))
            select_all.select_by_value("-1")
            
            # 解析
            soup = BeautifulSoup(browser.page_source, "lxml")
            table = soup.find("table", {"id": "report-table"})
            tbody = table.find("tbody")
            trs = tbody.find_all("tr")
            sql_val = list()
            for tr in trs:
                td = tr.find_all("td")
                row = self.sql_val(td)
                sql_val.append(row)

            # insert
            self._db.dividend_executemany("REPLACE INTO `twsd`.`dividend`(`stock_code`,`stock_name`,`dividend_date`,`dividend_year`,`dividend_month`,`dividend_day`,`declare_dividend_share_price`,`before_dividend_share_price`,`after_dividend_share_price`,`dividend`,`dividend_type`,`dividend_status`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", sql_val)
        except Exception as e:
            print(e)
        finally:
            browser.quit()
            print("stop twt49u")
        
    def sql_val(self, td):
        stock_code = td[1].text
        stock_name = td[2].text
        d = td[0].text
        yyy = d.split('年')
        dividend_year = int(yyy[0]) + 1911
        mm = yyy[1].split('月')
        dividend_month = int(mm[0])
        dd = mm[1].split('日')
        dividend_day = int(dd[0])
        dividend_date = str(dividend_year) + mm[0] + dd[0]
        declare_dividend_share_price = None
        if td[13].text != '':
            td13 = td[13].text.replace(',', '')
            declare_dividend_share_price = float(td13)
        before_dividend_share_price = None
        if td[3].text != '':
            td3 = td[3].text.replace(',', '')
            before_dividend_share_price = float(td3)
        after_dividend_share_price = None
        if td[4].text != '':
            td4 = td[4].text.replace(',', '')
            after_dividend_share_price = float(td4)
        dividend = None
        if td[5].text != '':
            td5 = td[5].text.replace(',', '')
            dividend = float(td5)
        dividend_type = 0
        txt6 = td[6].text
        if txt6 == '息':
            dividend_type = 2
        elif txt6 == '權':
            dividend_type = 1
        elif txt6 == '權息':
            dividend_type = 3
        row = (stock_code, stock_name, dividend_date, dividend_year, dividend_month, dividend_day, declare_dividend_share_price, before_dividend_share_price, after_dividend_share_price, dividend, dividend_type, 1)
        return row
