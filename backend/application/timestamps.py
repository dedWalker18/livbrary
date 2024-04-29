from datetime import datetime as dt
from datetime import date

def current_timestamp():
    current_time = dt.now()
    datetime_str = current_time.strftime('%Y-%m-%dT%H:%M')
    return datetime_str


def convert_datetime(datetime_value):

    datetime_object = dt.strptime(datetime_value, '%Y-%m-%dT%H:%M')
    return datetime_object


def date_today():
    return date.today()