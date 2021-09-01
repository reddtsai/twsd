from browser import chrome
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import time

class T108_SB19_Service:
    __url = 'https://mops.twse.com.tw/mops/web/t108sb19_q1'

    def get_dividend_declare_date(self, stock_code, yyy):
        cb = chrome.Chrome_Browser()
        cb.new_chrome_browser()
        declare_date = ''
        try:
            cb.Browser.get(self.__url)
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