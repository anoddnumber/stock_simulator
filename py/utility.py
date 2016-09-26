"""
Contains useful methods for the entire application
"""

import datetime


def is_within_stock_hours(time=None):
    """
    NASDAQ and NYSE are open from 9:30 AM - 4:00 PM EST (not including after hours trading)
    This translates to 1:30 PM - 8:00 PM UTC
    1:30 PM UTC will return True, 8:00 PM UTC will return False

    If time is None, use the current time

    :return: True if the time is within stock hours, otherwise False
    """

    if time is None:
        time = datetime.datetime.utcnow()

    # time.weekday -> 0 = Monday, 6 = Sunday
    return time.weekday() < 5 and time.hour == 13 and time.minute >= 30 or 14 <= time.hour < 20


def is_within_after_stock_hours(time=None):
    """
    Different sources say different time periods for after hours stock trading.
    Here, we will consider it to be 4:00 PM - 6:00 PM EST
    This translates to 8:00 PM - 10:00 PM UTC
    8:00 PM UTC will return True, 10:00 PM UTC will return False

    :return: True if the time is within after stock hours, otherwise False
    """

    if time is None:
        time = datetime.datetime.utcnow()

    # time.weekday -> 0 = Monday, 6 = Sunday
    return time.weekday() < 5 and 20 <= time.hour < 22
