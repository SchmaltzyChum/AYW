"""
Try to implement the Idea of an Event based stock time line.

To detect Peaks and troughs:
https://python.stockindicators.dev/indicators/ZigZag/
Also necesseary: https://python.stockindicators.dev/guide/#historical-quotes

To get news data related to the stock market:
https://www.marketaux.com/documentation

TODO: Check the get_peaks_and_trough function for the funcionality and correctness.
"""

import http.client, urllib.parse
from stock_indicators.indicators.common.quote import Quote
from api import FinancialDataAPI
from api import print_object_attributes
from stock_indicators import indicators
from stock_indicators import EndType
from datetime import datetime

findata = FinancialDataAPI()

def get_peaks_and_troughs(scheme:str = "VALOR_BC", listings: list = ["1222171_4"], from_date:str = "2022-07-01", to_date:str = '', threshold=3):
    """Find the peaks and troughs of a stock timeseries"""
    quotes = get_quote(scheme, listings, from_date, to_date)
    results = indicators.get_zig_zag(quotes, EndType.CLOSE, threshold)

    return results

def get_quote(scheme:str = "", listings: list = [""], from_date:str = "", to_date:str = ''):
    """Store the timeseries as a quote"""
    obj = findata.listing_EoDTimeseries(scheme, listings, from_date)
    quotes_list = [
        Quote(d, o, h, l, c, v)
        for d, o, h, l, c, v
        in zip([datetime.strptime(obj.data.listings[0].marketData.eodTimeseries[0].sessionDate, '%Y-%m-%d')], [obj.data.listings[0].marketData.eodTimeseries[0].open],
               [obj.data.listings[0].marketData.eodTimeseries[0].high], [obj.data.listings[0].marketData.eodTimeseries[0].low],
               [obj.data.listings[0].marketData.eodTimeseries[0].close], [obj.data.listings[0].marketData.eodTimeseries[0].volume])
    ]

    return quotes_list

def get_stock_news(company_symbol):
    """ Get stock news for this specify company.
    Due to free Version we are limit to 3 Articles per request:

    More information: https://www.marketaux.com/documentation
    """
    conn = http.client.HTTPSConnection('api.marketaux.com')

    params = urllib.parse.urlencode({
        'api_token': 'YRUBKUItIoeVYu8hzhZz8W2pfZ2PZPtz2PFruNuI',
        'symbols': company_symbol,
        'limit': 3,
        'published_on': '2023-01-23',
        })

    conn.request('GET', '/v1/news/all?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    print(data.decode('utf-8'))

