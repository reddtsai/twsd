from db import mysql
import requests

# 個股日成交資訊
class Stock_Day_Service:
    __url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date}&stockNo={code}'

    __db = None
    __sql = """REPLACE INTO `twsd`.`quote`
    (`stock_code`, `quote_date`, `opening_price`, `closing_price`, `highest_price`, `lowest_price`)
    VALUES(%s, %s, %s, %s, %s, %s)"""


    def __init__(self):
        self.__db = mysql.TWSD_DB()
        self.__db.connect()
    

    def collection(self, stock_code, trans_date):
        print("start collecting stock price")
        try:
            # 個股日成交
            response = requests.get(self.__url.format(date = trans_date, code = stock_code))
            j = response.json()
            assert 'stat' in j, 'NON'
            assert j['stat'] == 'OK', 'NON'

            # 解析
            sql_val = list()
            for data in j['data']:
                dd = data[0].split('/')
                yyyy = int(dd[0]) + 1911
                quote_date = str(yyyy) + dd[1] + dd[2]
                opening_price = float(data[3])
                closing_price = float(data[6])
                highest_price = float(data[4])
                lowest_price = float(data[5])
                row = (stock_code, quote_date, opening_price, closing_price, highest_price, lowest_price)
                sql_val.append(row)

            # insert
            if len(sql_val) > 0:
                self.__db.executemany(self.__sql, sql_val)

            response.close()
        except Exception as e:
            print(e)
        finally:
            print("stop collecting stock price")