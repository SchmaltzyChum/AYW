"""
Implemented an event based stock time line.

To detect Peaks and troughs:
https://python.stockindicators.dev/indicators/ZigZag/
https://python.stockindicators.dev/guide/#historical-quotes

To get news data related to the stock market:
https://www.marketaux.com/documentation
"""

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

def get_articles_dataframe_related_to_peaks(df, token="", percent_changes=3):
    """
    Get articles where are peaks or trough were detected in the dataframe.
    Create a Dataframe with the date of the peaks and the related news articles to this peak.
    :param df: Dataframe. Must be a stock market related frame.
    :param percent_changes:int In which range the stock price can move before get detected as a peak or trough
    :return: Dataframe with date of peak, 3 articles title and 3 urls related to the peak.
    """
    zigzag = get_peaks_and_troughs(df, percent_changes=percent_changes)
    pointtype = []
    for point in zigzag:
        pointtype.append(point.point_type)
    df.insert(0, "point_type", pointtype)
    date_series = df.loc[df.loc[:, "point_type"].isin(["H", "L"]), "date"]
    df.set_index("date", inplace=True)
    s = [get_stock_news('SIX', date=x, token=token) for x in date_series]
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
    """
    Drop empty rows
    :param df: Dataframe
    :return: Cleaned Dataframe
    """
    df = df.dropna(subset=['open'])
    return df

def set_df(obj):
    """
    Create a dataframe out of the financal data we get from the FinancalAPI of SIX.
    :param obj:findata from FinancialAPI
    :return: Data frame
    """
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
    """
    Detect the peaks and troughs of stock market graph. The dataframe must include following coloumns: date, open, high, low, close, volume.
    :param df: Data frame of stock market graph.
    :param percent_changes:int In which range the stock price can move before get detected as a peak or trough
    :return: List of Peak/Trough Points. See more: https://python.stockindicators.dev/indicators/ZigZag/
    """
    quotes = get_quote(df)
    results = indicators.get_zig_zag(quotes, EndType.CLOSE, percent_change=percent_changes)

    return results

def get_quote(df):
    """
    Helper function to create Quotes from a stock market data frame to detect peaks and troughs later.
    :param df: Data frame of stock market information
    :return: The quote list
    """
    quotes_list = [
        Quote(d, o, h, l, c, v)
        for d, o, h, l, c, v
        in zip(df['date'], df['open'], df['high'], df['low'], df['close'], df['volume'])
        ]
    return quotes_list

def get_stock_news(company_symbol, date, time_range=7, limit_of_articles=3, token=""):
    """
    Get stock news of a specific company for this specific date in a given time_range.
    Using the API of marketaux to get news related to stock market.
    More Information: https://www.marketaux.com/documentation

    :param company_symbol:str The company symbol.
    :param date:str The date of the news
    :param time_range:int Days.
    :param limit_of_articles: How much articles should be showed.
    :param token: The API token for the access to marketaux
    :return: A dictonary of news articles for the given company for this date range. You find all parameters in the API Doc.
    """
    after_date = date - timedelta(days=time_range)
    date = date.strftime('%Y-%m-%d')
    after_date = after_date.strftime('%Y-%m-%d')

    conn = http.client.HTTPSConnection('api.marketaux.com')

    params = urllib.parse.urlencode({
        'api_token': token,
        'symbols': company_symbol,
        'limit': limit_of_articles,
        'published_after': after_date,
        'published_before': date,
        })

    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    #print(data.decode('utf-8'))

    return json.loads(data.decode('utf-8'))
