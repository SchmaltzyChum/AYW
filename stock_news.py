import http.client, urllib.parse
from collections import OrderedDict

from stock_indicators.indicators.common.quote import Quote
from api import FinancialDataAPI
from api import print_object_attributes
from stock_indicators import indicators
from stock_indicators import EndType
from datetime import datetime, timedelta
import pandas as pd

#findata = FinancialDataAPI()

def clean_df(df):
    df = df.dropna(subset=['open'])
    return df

def set_df(obj):
    data = OrderedDict({
        'date': [],
        'open': [],
        'close': [],
        'low': [],
        'high': [],
        'volume': []
    })

    for eod in obj.data.listings[0].marketData.eodTimeseries:
        data['date'].append(datetime.strptime(eod.sessionDate, "%Y-%m-%d"))
        data['open'].append(eod.open if hasattr(eod, 'open') else None)
        data['close'].append(eod.close if hasattr(eod, 'close') else None)
        data['low'].append(eod.low if hasattr(eod, 'low') else None)
        data['high'].append(eod.high if hasattr(eod, 'high') else None)
        data['volume'].append(eod.volume if hasattr(eod, 'volume') else None)
    df = pd.DataFrame(data)
    return df

def get_peaks_and_troughs(df, percent_changes=3):
    quotes = get_quote(df)
    results = indicators.get_zig_zag(quotes, EndType.CLOSE, percent_change=percent_changes)

    return results

def get_quote(df):
    quotes_list = [
        Quote(d, o, h, l, c, v)
        for d, o, h, l, c, v
        in zip(df['date'], df['open'], df['high'], df['low'], df['close'], df['volume'])
        ]
    return quotes_list

def get_stock_news(company_symbol, date, time_range=7):
    after_date = date - timedelta(days=time_range)
    date = date.strftime('%Y-%m-%d')
    after_date = after_date.strftime('%Y-%m-%d')

    conn = http.client.HTTPSConnection('api.marketaux.com')

    params = urllib.parse.urlencode({
        'api_token': 'YRUBKUItIoeVYu8hzhZz8W2pfZ2PZPtz2PFruNuI',
        'symbols': company_symbol,
        'limit': 3,
        'published_after': after_date,
        'published_before': date,
        })

    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    print(data.decode('utf-8'))

