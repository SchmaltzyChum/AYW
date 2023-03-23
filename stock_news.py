import http.client, urllib.parse
from collections import OrderedDict

from stock_indicators.indicators.common.quote import Quote
from api import FinancialDataAPI
from api import print_object_attributes
from stock_indicators import indicators
from stock_indicators import EndType
from datetime import datetime, timedelta
import pandas as pd
import json

#findata = FinancialDataAPI()

def get_articels_dataframe_related_to_peaks(df):
    zigzag = get_peaks_and_troughs(df, percent_changes=3)
    pointtype = []
    for point in zigzag:
        pointtype.append(point.point_type)
    df.insert(0, "point_type", pointtype)
    date_series = df.loc[df.loc[:, "point_type"].isin(["H", "L"]), "date"]
    df.set_index("date", inplace=True)
    s = [get_stock_news('SIX', date=x) for x in date_series]
    title1 = []
    title2 = []
    title3 = []
    url1 = []
    url2 = []
    url3 = []
    for articels in s:
        if articels["meta"]["found"] <= 0:
            title1.append("No Article Found")
            title2.append("No Article Found")
            title3.append("No Article Found")
            url1.append("No URL Found")
            url2.append("No URL Found")
            url3.append("No URL Found")
        elif articels["meta"]["found"] == 1:
            title1.append(articels["data"][0]["title"])
            title2.append("No Article Found")
            title3.append("No Article Found")
            url1.append(articels["data"][0]["url"])
            url2.append("No URL Found")
            url3.append("No URL Found")
        elif articels["meta"]["found"] == 2:
            title1.append(articels["data"][0]["title"])
            title2.append(articels["data"][1]["title"])
            title3.append("No Article Found")
            url1.append(articels["data"][0]["url"])
            url2.append(articels["data"][1]["url"])
            url3.append("No URL Found")
        else:
            title1.append(articels["data"][0]["title"])
            title2.append(articels["data"][1]["title"])
            title3.append(articels["data"][2]["title"])
            url1.append(articels["data"][0]["url"])
            url2.append(articels["data"][1]["url"])
            url3.append(articels["data"][2]["url"])

    frame = {
        'date': date_series,
        'article1': title1,
        'article2': title2,
        'article3': title3,
        'url1': url1,
        'url2': url2,
        'url3': url3,
    }
    return pd.DataFrame(frame)

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

def get_stock_news(company_symbol, date, time_range=7, limit_of_articles=3):
    after_date = date - timedelta(days=time_range)
    date = date.strftime('%Y-%m-%d')
    after_date = after_date.strftime('%Y-%m-%d')

    conn = http.client.HTTPSConnection('api.marketaux.com')

    params = urllib.parse.urlencode({
        'api_token': 'hMrwMsRcY48HdSYN6a95fRjAPApWtEogIYEI4Evh',
        'symbols': company_symbol,
        'limit': limit_of_articles,
        'published_after': after_date,
        'published_before': date,
        })

    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    print(data.decode('utf-8'))

    return json.loads(data.decode('utf-8'))
