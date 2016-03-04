# -*- coding: utf-8 -*-

import re

class Checkers(object):

    def __init__(self):
        pass

    @staticmethod
    def _matched(pattern, string):
        if re.search(pattern, string) is None:
            return False
        else:
            return True

    @staticmethod
    def isvalid_year(yearstr):
        return Checkers._matched(r"^2[0|1][0-9][0-9]$", yearstr)

    @staticmethod
    def isvalid_month(monthstr):
        return Checkers._matched(r"^[0-9]{1}$|11|12", monthstr)

    @staticmethod
    def isvalid_day(daystr):
        return Checkers._matched(r"^[0-9]{1}$|^[1-2][0-9]$|30|31", daystr)

    @staticmethod
    def isvalid_usage(usagestr):
        return Checkers._matched(r"^[1|2|3|4]$", usagestr)

    @staticmethod
    def isvalid_kind(kindstr):
        return Checkers._matched(r"^[d|e]$", kindstr)

    @staticmethod
    def isvalid_amount(amountstr):
        return Checkers._matched(r"^[0-9]+(\s*[\+\-\*\/]?\s*[0-9]*)*$", amountstr)

    @staticmethod
    def isvalid_confirm(confstr):
        return Checkers._matched(r"^y|n$", confstr)

    @staticmethod
    def isvalid_id(idstr):
        return Checkers._matched(r"[0-9]+", idstr)