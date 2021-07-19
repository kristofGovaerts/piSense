from datetime import datetime


def current_time():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def timestr_to_delta(timestr):
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")


def is_active(timestamps, f=30, t=20):
    """
    Determine whether or not there is active (high-frequency) motion in a list of timestamps.
    :param timestamps: A list of timestamps, should be ordered chronologically.
    :param f: An int. Frequency threshold. If there are more timestamps per minute than f, function returns True.
    False otherwise.
    :param t: An int. Determines the minimum amount of observations necessary. If len(timestamps) < t, function will
    return False.
    :return: True or False.
    """
    n = len(timestamps)

    if n < t or timestamps[0] is None:
        out = False
    else:
        delta = timestr_to_delta(timestamps[-1]) - timestr_to_delta(timestamps[0])
        freq = n/(delta.total_seconds()/60)  # convert to per min rather than per sec
        if freq >= f:
            print(freq)
            out = True
        else:
            print(freq)
            out = False

    return out
