#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint

from bookDB import BookDBManager

class QuickViewer(object):

    def __init__(self):
        self.db = BookDBManager()

    def view(self):
        l = self.db.get_latest_20_records()
        pprint.pprint(list(reversed(l)))