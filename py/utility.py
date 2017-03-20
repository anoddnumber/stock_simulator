"""
Contains useful methods for the entire application
"""

import datetime
import threading


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


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def merge_two_dicts_recursive(a, b, path=None):
    """
    Merges two dictionaries together. Also merges the dictionaries within the dictionary if they have the same key.
    Example:
    a = {'a': {'blah': 'clah'}}
    b = {'a': {'foo': 'bar'}}

    The result of merge_two_dicts_recursive(a,b) would be
    {'a': {'blah': 'clah', 'foo': 'bar'}}
    """
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_two_dicts_recursive(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def merge_n_dicts(dict_list):
    "Not the most efficient.."
    result = {}
    for d in dict_list:
        result = merge_two_dicts(result, d)
    return result

def merge_n_dicts_recursive(dict_list):
    "Not the most efficient.."
    result = {}
    for d in dict_list:
        result = merge_two_dicts(result, d)
    return result

def do_every(interval, worker_func, iterations=0):
    """
    Runs a function every interval number of seconds

    :param interval: How often the function should run, in number of seconds
    :param worker_func: The function to run
    :param iterations: Number of iterations to do before stopping, defaults to infinite
    """
    if iterations != 1:
        t = threading.Timer(
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations-1]
        )
        t.setDaemon(True)
        t.start()

    worker_func()
    return t
