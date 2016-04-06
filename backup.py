#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

class AutoBackup(object):

    def __init__(self):
        pass

    @staticmethod
    def backup():
        cmd1 = "git add books/*"
        cmd2 = "git add db/*"
        cmd3 = "git commit -m \"Backup\""

        subprocess.call(cmd1.strip().split(" "))
        subprocess.call(cmd2.strip().split(" "))
        subprocess.call(cmd3.strip().split(" "))

if __name__ == '__main__':
    AutoBackup.backup()