import unittest
from base_unit_test import BaseUnitTest
from py import utility
import datetime


class TestUtilities(BaseUnitTest):

    def test_is_within_stock_hours(self):
        print "test_is_within_stock_hours"

        date = datetime.datetime(2016, 8, 27, 13, 30)  # Saturday
        result = utility.is_within_stock_hours(date)
        assert result is False

        date = datetime.datetime(2016, 8, 28, 13, 30)  # Sunday
        result = utility.is_within_stock_hours(date)
        assert result is False

        date = datetime.datetime(2016, 8, 29, 13, 30)  # Monday
        result = utility.is_within_stock_hours(date)
        assert result is True

        date = datetime.datetime(2016, 8, 29, 20)  # Monday
        result = utility.is_within_stock_hours(date)
        assert result is False

    def test_is_within_after_stock_hours(self):
        print "test_is_within_after_stock_hours"

        date = datetime.datetime(2016, 8, 27, 20)  # Saturday
        result = utility.is_within_stock_hours(date)
        assert result is False

        date = datetime.datetime(2016, 8, 28, 20)  # Sunday
        result = utility.is_within_after_stock_hours(date)
        assert result is False

        date = datetime.datetime(2016, 8, 29, 20)  # Monday
        result = utility.is_within_after_stock_hours(date)
        assert result is True

        date = datetime.datetime(2016, 8, 29, 21, 59)  # Monday
        result = utility.is_within_after_stock_hours(date)
        assert result is True

        date = datetime.datetime(2016, 8, 29, 22)  # Monday
        result = utility.is_within_after_stock_hours(date)
        assert result is False

if __name__ == '__main__':
    unittest.main()
