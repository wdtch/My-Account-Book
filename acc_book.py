#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from dateutil.relativedelta import relativedelta
import readline

from backup import AutoBackup
from calc import Calculator
from checker import Checkers
from bookDB import BookDBManager
import export


# デフォルトの入力テキストを指定できるように拡張されたinput()
def rlinput(prompt, prefill=""):
    readline.set_startup_hook(lambda: readline.insert_text(str(prefill)))
    try:
        return input(prompt)
    finally:
        readline.set_startup_hook()


class AccBook(object):

    """家計簿を管理するクラス"""

    def __init__(self):
        self.year = ""
        self.month = ""
        self.day = ""
        self.kind = ""
        self.usage = ""
        self.detail = ""
        self.amount = ""
        self.bookDB = BookDBManager()

    def record(self):
        self._input_year()

    def _input_year(self):
        year = rlinput("年を入力してください。\n"
                     "> ")
        if Checkers.isvalid_year(year):
            self.year = year
            self._input_month()
        else:
            print("入力が不正です。")
            self._input_year()

    def _input_month(self):
        month = rlinput("\n"
                      "月を入力してください。\n"
                      "> ")
        if Checkers.isvalid_month(month):
            self.month = month
            self._input_day()
        else:
            print("入力が不正です。")
            self._input_month()

    def _input_day(self):
        day = rlinput("\n"
                    "日を入力してください。\n"
                    "> ")
        if Checkers.isvalid_day(day):
            self.day = day
            self._input_usage()
        else:
            print("入力が不正です。")
            self._input_day()

    def _input_usage(self):
        usage = rlinput("\n"
                      "用途を選択し、数字を入力してください。\n"
                      "1. 交通費\n"
                      "2. 食費\n"
                      "3. 日用品・雑貨\n"
                      "4. その他\n"
                      "> ")
        if Checkers.isvalid_usage(usage):
            if usage == "1":
                self.usage = "交通費"
            elif usage == "2":
                self.usage = "食費"
            elif usage == "3":
                self.usage = "日用品・雑貨"
            elif usage == "4":
                self.usage = "その他"
            self._input_kind()
        else:
            print("入力が不正です。")
            self._input_usage()

    def _input_kind(self):
        kind = rlinput("\n"
                     "支出の種類を入力してください。\n"
                     "dailyの\"d\"または、extraの\"e\"を入力してください。\n"
                     "> ")
        if Checkers.isvalid_kind(kind):
            if kind == "d":
                self.kind = "daily"
            elif kind == "e":
                self.kind = "extra"
            self._input_detail()
        else:
            print("入力が不正です。")
            self._input_kind()

    def _input_detail(self):
        detail = rlinput("\n"
                       "内訳を入力してください。\n"
                       "> ")
        self.detail = detail
        self._input_amount()

    def _input_amount(self):
        amount = rlinput("\n"
                       "金額を入力してください。四則演算の計算式でも構いません。\n"
                       "> ")
        if Checkers.isvalid_amount(amount):
            calculator = Calculator()
            self.amount = str(calculator.calc(amount))
            self._confirm()
        else:
            print("入力が不正です。")
            self._input_amount()

    def _confirm(self):
        print("入力内容は以下の通りです。正しければyを、訂正があればnを入力してください。\n" + \
              "日時\n" + \
              "{0}/{1}/{2}\n".format(self.year, self.month, self.day) + \
              "種類\n" + \
              self.kind + "\n" + \
              "用途\n" + \
              self.usage + "\n" + \
              "内訳\n" + \
              self.detail + "\n" + \
              "金額\n" + \
              self.amount)

        ok_or_not = rlinput("> ")
        if Checkers.isvalid_confirm(ok_or_not):
            if ok_or_not == "y":
                self.write()
            else:
                print("初めに戻ります。")
                self._input_year()
        else:
            print("入力が不正です。")
            self._confirm()

    def write(self):
        # テーブルの存在確認
        for_existence = "SELECT name FROM sqlite_master;"
        self.bookDB.dbcur.execute(for_existence)

        checked_table_name = "book"
        if checked_table_name in [v[0] for v in self.bookDB.dbcur]:
            pass
        else:
            # テーブルが存在しなければ作成
            self.bookDB.dbcur.execute(
                "CREATE TABLE book(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, year INTEGER, month INTEGER, day INTEGER, kind TEXT, usage TEXT, detail TEXT, amount INTEGER);")

        # 書き込み
        self.bookDB.dbcur.execute(
            "INSERT INTO book(year, month, day, kind, usage, detail, amount) VALUES (?, ?, ?, ?, ?, ?, ?);", (self.year, self.month, self.day, self.kind, self.usage, self.detail, self.amount))

        # 変更を保存
        self.bookDB.dbcon.commit()
        # 後処理
        self.bookDB.dbcon.close()

        # 自動バックアップ
        AutoBackup.backup_db()

    def browse_balance(self,
                        year=datetime.date.today().year,
                        month=datetime.date.today().month,
                        day=datetime.date.today().day):
        # 残高のスタート値
        daily_base = 2500
        extra_base = 15000

        # 14日以前は前月15日〜の残高を表示するように調整
        if day <= 14:
            month -= 1
        daily_w1 = self.bookDB.get_daily_balance_week1(year, month)
        daily_w2 = self.bookDB.get_daily_balance_week2(year, month)
        daily_w3 = self.bookDB.get_daily_balance_week3(year, month)
        daily_w4 = self.bookDB.get_daily_balance_week4(year, month)
        extra = self.bookDB.get_extra_balance(year, month)


        # 残高一覧を出力
        print("daily - week 1: {}".format(daily_base - daily_w1))
        print("daily - week 2: {}".format(daily_base - daily_w2))
        print("daily - week 3: {}".format(daily_base - daily_w3))
        print("daily - week 4: {}".format(daily_base - daily_w4))
        print("extra: {}".format(extra_base - extra))

    def delete(self, record_id):
        """指定されたIDを持つレコードを削除する"""
        # IDに合致するレコードを取ってくる
        self.bookDB.dbcur.execute("SELECT * FROM book WHERE id = ?;", (record_id,))
        record = self.bookDB.dbcur.fetchone()

        if record is None:
            print("そのレコードは存在しません。")
            return
        else:
            # 確認
            print("以下のレコードを削除します。よろしければyを、削除をキャンセルするならnを入力してください。\n" + \
                  "年: {}\n".format(record[1])  + \
                  "月: {}\n".format(record[2]) + \
                  "日: {}\n".format(record[3]) + \
                  "種類: {}\n".format(record[4]) + \
                  "用途: {}\n".format(record[5]) + \
                  "内訳: {}\n".format(record[6]) + \
                  "金額: {}".format(record[7]))

            ok_or_not = rlinput("> ")
            if Checkers.isvalid_confirm(ok_or_not):
                if ok_or_not == "y":
                    self.bookDB.dbcur.execute("DELETE FROM book WHERE id = ?;", (record_id,))
                    # 変更を保存
                    self.bookDB.dbcon.commit()
                    # 後処理
                    self.bookDB.dbcon.close()

                    # 変更をバックアップ
                    AutoBackup.backup_db()
                else:
                    print("初めに戻ります。")
                    return
            else:
                print("入力が不正です。")
                self.delete(record_id)

    def modify(self, record_id):
        # IDに合致するレコードを取ってくる
        self.bookDB.dbcur.execute("SELECT * FROM book WHERE id = ?;", (record_id,))
        record = self.bookDB.dbcur.fetchone()

        if record is None:
            print("そのレコードは存在しません。")
            return
        else:
            self.year = record[1]
            self.month = record[2]
            self.day = record[3]
            self.kind = record[4]
            self.usage = record[5]
            self.detail = record[6]
            self.amount = record[7]
            # 確認
            print("以下のレコードを修正します。よろしければyを、削除をキャンセルするならnを入力してください。\n" + \
                  "年: {}\n".format(self.year)  + \
                  "月: {}\n".format(self.month) + \
                  "日: {}\n".format(self.day) + \
                  "種類: {}\n".format(self.kind) + \
                  "用途: {}\n".format(self.usage) + \
                  "内訳: {}\n".format(self.detail) + \
                  "金額: {}".format(self.amount))

            ok_or_not = rlinput("> ")
            if Checkers.isvalid_confirm(ok_or_not):
                if ok_or_not == "y":
                    print("修正内容を入力してください。")
                    self._modify_year(record_id)
                    # 変更を保存
                    self.bookDB.dbcon.commit()
                    # 後処理
                    self.bookDB.dbcon.close()

                    # 変更をバックアップ
                    AutoBackup.backup_db()
                else:
                    print("初めに戻ります。")
                    return
            else:
                print("入力が不正です。")
                self.modify(record_id)

    def _modify_year(self, record_id):
        year = rlinput("年を入力してください。\n"
                     "> ", self.year)
        if Checkers.isvalid_year(year):
            self.year = year
            self._modify_month(record_id)
        else:
            print("入力が不正です。")
            self._modify_year(record_id)

    def _modify_month(self, record_id):
        month = rlinput("\n"
                      "月を入力してください。\n"
                      "> ", self.month)
        if Checkers.isvalid_month(month):
            self.month = month
            self._modify_day(record_id)
        else:
            print("入力が不正です。")
            self._modify_month(record_id)

    def _modify_day(self, record_id):
        day = rlinput("\n"
                    "日を入力してください。\n"
                    "> ", self.day)
        if Checkers.isvalid_day(day):
            self.day = day
            self._modify_usage(record_id)
        else:
            print("入力が不正です。")
            self._modify_day(record_id)

    def _modify_usage(self, record_id):
        usage = rlinput("\n"
                      "用途を選択し、数字を入力してください。\n"
                      "1. 交通費\n"
                      "2. 食費\n"
                      "3. 日用品・雑貨\n"
                      "4. その他\n"
                      "> ", self.usage)
        if Checkers.isvalid_usage(usage):
            if usage == "1":
                self.usage = "交通費"
            elif usage == "2":
                self.usage = "食費"
            elif usage == "3":
                self.usage = "日用品・雑貨"
            elif usage == "4":
                self.usage = "その他"
            self._modify_kind(record_id)
        else:
            print("入力が不正です。")
            self._modify_usage(record_id)

    def _modify_kind(self, record_id):
        kind = rlinput("\n"
                     "支出の種類を入力してください。\n"
                     "dailyの\"d\"または、extraの\"e\"を入力してください。\n"
                     "> ", self.kind[0])
        if Checkers.isvalid_kind(kind):
            if kind == "d":
                self.kind = "daily"
            elif kind == "e":
                self.kind = "extra"
            self._modify_detail(record_id)
        else:
            print("入力が不正です。")
            self._modify_kind(record_id)

    def _modify_detail(self, record_id):
        detail = rlinput("\n"
                       "内訳を入力してください。\n"
                       "> ", self.detail)
        self.detail = detail
        self._modify_amount(record_id)

    def _modify_amount(self, record_id):
        amount = rlinput("\n"
                       "金額を入力してください。四則演算の計算式でも構いません。\n"
                       "> ", self.amount)
        if Checkers.isvalid_amount(amount):
            calculator = Calculator()
            self.amount = str(calculator.calc(amount))
            self._confirm_modification(record_id)
        else:
            print("入力が不正です。")
            self._modify_amount(record_id)

    def _confirm_modification(self, record_id):
        print("修正内容は以下の通りです。正しければyを、訂正があればnを入力してください。\n" + \
              "日時\n" + \
              "{0}/{1}/{2}\n".format(self.year, self.month, self.day) + \
              "種類\n" + \
              self.kind + "\n" + \
              "用途\n" + \
              self.usage + "\n" + \
              "内訳\n" + \
              self.detail + "\n" + \
              "金額\n" + \
              self.amount)

        ok_or_not = rlinput("> ")
        if Checkers.isvalid_confirm(ok_or_not):
            if ok_or_not == "y":
                self._write_modification(record_id)
            else:
                print("初めに戻ります。")
                self._modify_year(record_id)
        else:
            print("入力が不正です。")
            self._confirm_modification(record_id)

    def _write_modification(self, record_id):
        # 書き込み
        self.bookDB.dbcur.execute(
            "UPDATE book SET year = ?, month = ?, day = ?, kind = ?, usage = ?, detail = ?, amount = ? WHERE id = ?;", (self.year, self.month, self.day, self.kind, self.usage, self.detail, self.amount, record_id))

    def _auto_export(self):
        with open("startdate.txt") as f:
            current = datetime.datetime.now()
            last = datetime.datetime.strptime(f.readline().rstrip("\n"), "%Y/%m/%d")
            fifteen = datetime.datetime(last.year, last.month, 15)

            if current >= fifteen and last < fifteen:
                exporter = export.Exporter()
                exporter.export_markdown((current.date() - relativedelta(months=1)).year,
                                         (current.date() - relativedelta(months=1)).month)

    def _record_startdate(self):
        with open("startdate.txt", "w") as f:
            f.write(datetime.datetime.now().strftime("%Y/%m/%d"))

    def start(self):
        """起動時に必ず実行するメソッド"""
        # 家計簿自動エクスポート、起動日記録
        self._auto_export()
        self._record_startdate()