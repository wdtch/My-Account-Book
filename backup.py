#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

class AutoBackup(object):

    def __init__(self):
        pass

    @staticmethod
    def backup_books():
        cmd1 = "git add books/*"
        cmd2 = "git commit -m Auto-Backup"

        subprocess.call(cmd1.strip().split(" "))
        subprocess.call(cmd2.strip().split(" "))

    @staticmethod
    def backup_db():
        cmd1 = "git add db/*"
        cmd2 = "git commit -m Auto-Backup"

        subprocess.call(cmd1.strip().split(" "))
        subprocess.call(cmd2.strip().split(" "))

if __name__ == '__main__':
    AutoBackup.backup_books()
    AutoBackup.backup_db()