import mysql.connector
import configparser


class TWSD_DB:
    def __init__(self):
        cfg = configparser.ConfigParser()
        cfg.read("app.ini")
        self._host = cfg["mysql"]["host"]
        self._user = cfg["mysql"]["user"]
        self._password = cfg["mysql"]["password"]
        self._db = cfg["mysql"]["db"]
    
    # def __enter__(self):
    #     print("enter")

    # def __exit__(self, type, value, trace):
    #     print("__exit")

    def __del__(self):
        if self._conn is not None:
            self._conn.close()

    def connect(self):
        self._conn = mysql.connector.connect(
                host = self._host,
                user = self._user,
                password = self._password,
                database = self._db 
            )
    
    def fetchall(self, sql):
        with self._conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            for x in result:
                print(x)
        
    def dividend_executemany(self, sql, val):
        with self._conn.cursor() as cursor:
            cursor.executemany(sql, val)
            self._conn.commit()

