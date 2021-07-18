from datetime import datetime


def current_time():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def timestr_to_delta(timestr):
    return datetime.strptime(a, "%Y-%m-%d %H:%M:%S")
