''' Some helpers '''
from datetime import datetime, timedelta
from re import compile as re_compile

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

re_search = re_compile(r'(\d{1,2}) (minute|minutes|hour|hours) ago')


def aprox_time(time_cad, now=None):
    '''
        Depending on the post time, take the moment when created

        if 'just now' in cad, give the current time,
        else, extract the time pattern assuming,
        by instance: 4 minutes ago, '{value} {unit} ago'

        if not cad given or empty, return current time

        Parameters
        ----------
        time_cad : str
            string containing when post was created

        now: datetime
            optional, it's for testing the function

        Returns
        -------
        datetime
            the aprox moment as datetime
    '''

    params = {}

    if not now:
        now = datetime.now()

    if time_cad is None \
       or'just now' in time_cad \
       or time_cad.strip() == '':
        return now

    regex_result = re_search.search(time_cad)

    value, unit = regex_result.groups()
    _value = int(value)

    if 'minute' in unit:
        params['minutes'] = _value

    elif 'hour' in unit:
        params['hours'] = _value

    return now - timedelta(**params)


def add_30_minutes(ts):
    """Helper to add 30 minutes to a given time"""
    return ts + timedelta(minutes=30)


def plot_forecast(posts, forecast_set):
    # forecast_set = ln.predict(X_lately)

    posts['Forecast'] = np.nan

    last_date = posts.iloc[-1].time

    for i in forecast_set:
        last_date = last_date + timedelta(minutes=30)
        posts.loc[last_date] = [np.nan for _ in range(len(posts.columns)-1)] + [i]

    posts['count'].plot()
    posts['Forecast'].plot()
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.show()
        