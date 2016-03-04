# -*- coding: utf-8 -*-

import sqlite3

class BookDBManager(object):

    def __init__(self):
        self.dbcon = sqlite3.connect("db/book.db")
        self.dbcur = self.dbcon.cursor()

    def get_daily_balance_week1(self, year, month):
        # 年をまたぐときはイレギュラーな処理が必要
        if month == 12:
            # 1週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND year = ? AND ((month = 12 AND day >= 15) AND (month = 12 AND day <= 22));", (year,))
            daily_w1 = int(self.dbcur.fetchone()[0])
        # 年をまたがないとき
        else:
            # 1週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND year = ? AND ((month = ? AND day >= 15) AND (month = ? AND day <= 22));", (year, month, month))
            daily_w1 = int(self.dbcur.fetchone()[0])

        return daily_w1

    def get_daily_balance_week2(self, year, month):
        if month == 12:
            # 2週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND year = ? AND ((month = 12 AND day >= 23) AND (month = 12 AND day <= 29));", (year,))
            daily_w2 = int(self.dbcur.fetchone()[0])
        # 年をまたがないとき
        else:
            # 2週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND year = ? AND ((month = ? AND day >= 23) AND (month = ? AND day <= 29));", (year, month, month))
            daily_w2 = int(self.dbcur.fetchone()[0])

        return daily_w2

    def get_daily_balance_week3(self, year, month):
        if month == 12:
            # 3週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND (year = ? AND month = 12 AND day >= 30) OR (year = ? AND month = 1 AND day <= 7);", (year, year+1))
            daily_w3 = int(self.dbcur.fetchone()[0])
        # 年をまたがないとき
        else:
            # 3週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND year = ? AND ((month = ? AND day >= 30) OR (month = ? AND day <= 7));", (year, month, month+1))
            daily_w3 = int(self.dbcur.fetchone()[0])

        return daily_w3

    def get_daily_balance_week4(self, year, month):
        if month == 12:
            # 4週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND year = ? AND ((month = 1 AND day >= 8) AND (month = 1 AND day <= 14));", (year+1,))
            daily_w4 = int(self.dbcur.fetchone()[0])
        else:
            # 4週目の残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"daily\" AND year = ? AND ((month = ? AND day >= 8) AND (month = ? AND day <= 14));", (year, month+1, month+1))
            daily_w4 = int(self.dbcur.fetchone()[0])

        return daily_w4

    def get_extra_balance(self, year, month):
        if month == 12:
            # extraの残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"extra\" AND year = ? AND ((month = 12 AND day >= 15) OR (year = ? AND month = 1 AND day <= 14));", (year, year+1))
            extra = int(self.dbcur.fetchone()[0])
        else:
            # extraの残高合計
            self.dbcur.execute("SELECT total(amount) FROM book WHERE kind = \"extra\" AND year = ? AND ((month = ? AND day >= 15) OR (month = ? AND day <= 14));", (year, month, month+1))
            extra = int(self.dbcur.fetchone()[0])

        return extra

    def get_monthlyrecords(self, year, month):
        # 1月分のレコードをすべて取得する
        if month == 12:
            self.dbcur.execute("SELECT * FROM book WHERE (year = ? AND month = 12 AND day >= 15) OR (year = ? AND month = 1 AND day <= 14);", (year, year+1))
        else:
            self.dbcur.execute("SELECT * FROM book WHERE year = ? AND ((month = ? AND day >= 15) OR (month = ? AND day <= 14));", (year, month, month+1))

        return self.dbcur.fetchall()

    def get_latest_20_records(self):
        self.dbcur.execute("SELECT * FROM book ORDER BY id DESC LIMIT 20;")
        return self.dbcur.fetchall()