import unittest

import checker


class TestChecker(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_isvalid_year(self):
        valid1 = "2015"
        valid2 = "2016"
        valid3 = "2050"

        invalid1 = "205"
        invalid2 = "3016"
        invalid3 = "abc"
        invalid4 = "あいうえお"

        self.assertTrue(checker.Checkers.isvalid_year(valid1))
        self.assertTrue(checker.Checkers.isvalid_year(valid2))
        self.assertTrue(checker.Checkers.isvalid_year(valid3))

        self.assertFalse(checker.Checkers.isvalid_year(invalid1))
        self.assertFalse(checker.Checkers.isvalid_year(invalid2))
        self.assertFalse(checker.Checkers.isvalid_year(invalid3))
        self.assertFalse(checker.Checkers.isvalid_year(invalid4))

    def test_isvalid_month(self):
        valid1 = "1"
        valid2 = "4"
        valid3 = "12"

        invalid1 = "13"
        invalid2 = "26"
        invalid3 = "abc"
        invalid4 = "あいうえお"

        self.assertTrue(checker.Checkers.isvalid_month(valid1))
        self.assertTrue(checker.Checkers.isvalid_month(valid2))
        self.assertTrue(checker.Checkers.isvalid_month(valid3))

        self.assertFalse(checker.Checkers.isvalid_month(invalid1))
        self.assertFalse(checker.Checkers.isvalid_month(invalid2))
        self.assertFalse(checker.Checkers.isvalid_month(invalid3))
        self.assertFalse(checker.Checkers.isvalid_month(invalid4))

    def test_isvalid_day(self):
        valid1 = "1"
        valid2 = "18"
        valid3 = "31"

        invalid1 = "33"
        invalid2 = "56"
        invalid3 = "abc"
        invalid4 = "あいうえお"

        self.assertTrue(checker.Checkers.isvalid_day(valid1))
        self.assertTrue(checker.Checkers.isvalid_day(valid2))
        self.assertTrue(checker.Checkers.isvalid_day(valid3))

        self.assertFalse(checker.Checkers.isvalid_day(invalid1))
        self.assertFalse(checker.Checkers.isvalid_day(invalid2))
        self.assertFalse(checker.Checkers.isvalid_day(invalid3))
        self.assertFalse(checker.Checkers.isvalid_day(invalid4))

    def test_isvalid_usage(self):
        valid1 = "1"
        valid2 = "2"
        valid3 = "3"
        valid4 = "4"

        invalid1 = "5"
        invalid2 = "12"
        invalid3 = "abc"
        invalid4 = "あいうえお"

        self.assertTrue(checker.Checkers.isvalid_usage(valid1))
        self.assertTrue(checker.Checkers.isvalid_usage(valid2))
        self.assertTrue(checker.Checkers.isvalid_usage(valid3))
        self.assertTrue(checker.Checkers.isvalid_usage(valid4))

        self.assertFalse(checker.Checkers.isvalid_usage(invalid1))
        self.assertFalse(checker.Checkers.isvalid_usage(invalid2))
        self.assertFalse(checker.Checkers.isvalid_usage(invalid3))
        self.assertFalse(checker.Checkers.isvalid_usage(invalid4))

    def test_isvalid_kind(self):
        valid1 = "d"
        valid2 = "e"

        invalid1 = "3"
        invalid2 = "r"
        invalid3 = "df"
        invalid4 = "え"

        self.assertTrue(checker.Checkers.isvalid_kind(valid1))
        self.assertTrue(checker.Checkers.isvalid_kind(valid2))

        self.assertFalse(checker.Checkers.isvalid_kind(invalid1))
        self.assertFalse(checker.Checkers.isvalid_kind(invalid2))
        self.assertFalse(checker.Checkers.isvalid_kind(invalid3))
        self.assertFalse(checker.Checkers.isvalid_kind(invalid4))

    def test_isvalid_amount(self):
        valid1 = "100"
        valid2 = "200 + 500"
        valid3 = "1000 - 150"
        valid4 = "30*4"
        valid5 = "500/10"
        valid6 = "100 + 50 * 6"
        valid7 = "10000 - 2000 * 4 + 230"

        invalid1 = "5:/.22"
        invalid2 = "2a"
        invalid3 = "abc"
        invalid4 = "あいうえお"

        self.assertTrue(checker.Checkers.isvalid_amount(valid1))
        self.assertTrue(checker.Checkers.isvalid_amount(valid2))
        self.assertTrue(checker.Checkers.isvalid_amount(valid3))
        self.assertTrue(checker.Checkers.isvalid_amount(valid4))
        self.assertTrue(checker.Checkers.isvalid_amount(valid5))
        self.assertTrue(checker.Checkers.isvalid_amount(valid6))
        self.assertTrue(checker.Checkers.isvalid_amount(valid7))

        self.assertFalse(checker.Checkers.isvalid_amount(invalid1))
        self.assertFalse(checker.Checkers.isvalid_amount(invalid2))
        self.assertFalse(checker.Checkers.isvalid_amount(invalid3))
        self.assertFalse(checker.Checkers.isvalid_amount(invalid4))


if __name__ == '__main__':
    unittest.main(argv=["nose", '-v'])
