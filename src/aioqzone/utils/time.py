from datetime import date, datetime, timedelta
from pytz import timezone
import time

TIME_ZONE = timezone('Asia/Shanghai')


def time_ms(ts: float = None):
    """int timestamp in ms.

    Args:
        ts (float, optional): timestamp in seconds. Defaults to `time.time()`.

    Returns:
        int: ms timestamp
    """
    return round((ts or time.time()) * 1000)


def dayspac(ts1: float, ts2: float = None):
    """return ts2 - ts1

    Args:
        ts1 (float): past timestamp, in seconds, like `time.time()`
        ts2 (float, optional): timestamp, in seconds. Defaults to `time.time()`.

    Returns:
        float: dayspac in float
    """
    d = date.fromtimestamp(ts2 or time.time()) - date.fromtimestamp(ts1)
    return d.seconds / 86400


def approx_ts(timedesc: str):
    """Given a time description, returns an approximate timestamp."""
    timedesc = timedesc.strip()
    assert timedesc
    hashm = ':' in timedesc
    didx = timedesc.find('天')
    hmfmt = '%H:%M'

    if '日' in timedesc:
        # specific day
        fmt = '%Y年%m月%d日'
        dt = datetime.strptime(timedesc, fmt + hmfmt if hashm else fmt)
        return int(dt.replace(tzinfo=TIME_ZONE).timestamp())

    today = datetime.today().astimezone(TIME_ZONE)    # based on today
    if hashm:
        tm = datetime.strptime(timedesc[-5:], hmfmt).time()
        dt = today.replace(hour=tm.hour, minute=tm.minute)
        if didx == -1: return int(dt.timestamp())

        # day in delta
        assert didx > 0
        delta = timedelta(days={'昨': 1, '前': 2}[timedesc[didx - 1]])
        dt -= delta
        return int(dt.timestamp())

    # today
    dt = time.strptime(timedesc.strip(), hmfmt)
    return int(time.mktime(dt))
