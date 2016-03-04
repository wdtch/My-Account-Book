# -*- coding: utf-8 -*-

import sys

from bookDB import BookDBManager

class Exporter(object):
    """家計簿を各種形式でエクスポートするためのクラス"""

    def __init__(self):
        self.db = BookDBManager()

    def export_markdown(self, year, month):
        # タイトルを構成
        md = "#{0}年{1}月分の家計簿\n".format(year, month)

        # 残高を取得
        daily_w1 = self.db.get_daily_balance_week1(year, month)
        daily_w2 = self.db.get_daily_balance_week2(year, month)
        daily_w3 = self.db.get_daily_balance_week3(year, month)
        daily_w4 = self.db.get_daily_balance_week4(year, month)
        extra = self.db.get_extra_balance(year, month)

        # 残高を書き込み
        md += "## 残高  \n"
        if daily_w1 > 2500:
            md += "Daily 1週目: <span style=\"color:red\">{}</span>  \n".format(2500 - daily_w1)
        else:
            md += "Daily 1週目: {}  \n".format(2500 - daily_w1)

        if daily_w2 > 2500:
            md += "Daily 2週目: <span style=\"color:red\">{}</span>  \n".format(2500 - daily_w2)
        else:
            md += "Daily 2週目: {}  \n".format(2500 - daily_w2)

        if daily_w3 > 2500:
            md += "Daily 3週目: <span style=\"color:red\">{}</span>  \n".format(2500 - daily_w3)
        else:
            md += "Daily 3週目: {}  \n".format(2500 - daily_w3)

        if daily_w4 > 2500:
            md += "Daily 4週目: <span style=\"color:red\">{}</span>  \n".format(2500 - daily_w4)
        else:
            md += "Daily 4週目: {}  \n".format(2500 - daily_w4)

        if extra > 15000:
            md += "Extra: <span style=\"color:red\">{}</span>  \n".format(15000 - extra)
        else:
            md += "Extra: {}  \n".format(15000 - extra)

        # 内容を書き込み
        # 表のフォーマット
        md += "\n## 詳細\n" + \
              "| ID | 年 | 月 | 日 | 種類 | 用途 | 内訳 | 金額 |\n" + \
              "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
        records = self.db.get_monthlyrecords(year, month)
        for record in records:
            md += "|" + "|".join(map(str, record)) + "|" + "\n"

        # ファイルに書き込み
        with open("books/{0}_{1}.md".format(year, month), "w") as f:
            f.write(md)


if __name__ == '__main__':
    args = sys.argv
    year = int(args[1])
    month = int(args[2])

    exporter = Exporter()
    exporter.export_markdown(year, month)