#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint

from bookDB import BookDBManager

class QuickViewer(object):

    def __init__(self):
        self.db = BookDBManager()

    def view(self, num=20):
        l = self.db.get_latest_records(num)
        pprint.pprint(list(reversed(l)))