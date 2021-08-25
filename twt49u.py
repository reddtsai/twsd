from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

# Chrome Options
option = webdriver.ChromeOptions()
option.add_argument('--headless') 

def twt49u(from_year, from_month, from_date, to_year, to_month, to_date):
    print("start twt49u")
    # Chrome
    browser  = webdriver.Chrome(executable_path='./drivers/chromedriver', options=option)
    try:
        # 除權除息計算結果表
        browser.get('https://www.twse.com.tw/zh/page/trading/exchange/TWT49U.html')
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

        time.sleep(5)

        select_all = Select(browser.find_element_by_name("report-table_length"))
        select_all.select_by_value("-1")

        soup = BeautifulSoup(browser.page_source, "lxml")
        table = soup.find("table", {"id": "report-table"})
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        rows = list()
        for tr in trs:
            rows.append([td.text for td in tr.find_all("td")])

        print(rows)
        print(len(rows))
    except Exception as e:
        print(e)
    finally:
        browser.quit()
        print("stop twt49u")

twt49u("2021", "1", "1", "2021", "8", "23")