# -*- coding: utf-8 -*-

__doc__ = """::::: オレオレ家計簿 :::::

Usage:
  main.py
  main.py [-b | --balance] [<year>] [<month>]
  main.py [-d | --delete] [<id>]
  main.py [-e | --export] [<year>] [<month>]
  main.py [-h | --help]
  main.py [-q | --qview] [<num>]

Options:
  -b --balance  現在の残高を表示します。年月の指定があった場合は、その時点での残高を表示します。
  -d --delete   指定されたIDを持つレコードを削除します。
  -e --export   指定された年月の分の家計簿を出力します。
  -h --help     このヘルプを表示します。
  -q --qview    最新n件のレコードを一覧表示します。件数の指定がない場合は20件分を表示します。
"""


from docopt import docopt

import acc_book
from checker import Checkers
from export import Exporter
from quickview import QuickViewer


if __name__ == '__main__':
    accbook = acc_book.AccBook()
    accbook.start()

    args = docopt(__doc__)
    if args["--balance"]:
        if args["<year>"] is None and args["<month>"] is None:
            accbook.browse_balance()
        else:
            if Checkers.isvalid_year(args["<year>"]) and Checkers.isvalid_month(args["<month>"]):
                accbook.browse_balance(int(args["<year>"]), int(args["<month>"]))
            else:
                print("正しい年月を入力してください。")
    elif args["--delete"]:
        if args["<id>"] is not None and Checkers.isvalid_id(args["<id>"]):
            accbook.delete(int(args["<id>"]))
        else:
            print("正しいIDを入力してください。")
    elif args["--export"]:
        if Checkers.isvalid_year(args["<year>"]) and Checkers.isvalid_month(args["<month>"]):
            exporter = Exporter()
            exporter.export_markdown(int(args["<year>"]), int(args["<month>"]))
        else:
            print("正しい年月を入力してください。")
    elif args["--qview"]:
        q_viewer = QuickViewer()
        if args["<num>"] is None:
          q_viewer.view()
        else:
          q_viewer.view(int(args["<num>"]))
    else:
        accbook.record()