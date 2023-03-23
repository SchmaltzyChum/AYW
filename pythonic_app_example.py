import http.client, urllib.parse

import pandas

from stock_news import get_stock_news, get_peaks_and_troughs, set_df, clean_df
from api import  FinancialDataAPI



if __name__ == '__main__':
    findata = FinancialDataAPI()
    obj = findata.listing_EoDTimeseries(scheme="VALOR_BC", listings=["1222171_4"], from_date="2022-07-01")
    df = set_df(obj)
    df = clean_df(df)
    zigzag = get_peaks_and_troughs(df, percent_changes=3)
    pointtype=[]
    for point in zigzag:
        pointtype.append(point.point_type)
    df.insert(0, "point_type", pointtype)
    date_series = df.loc[df.loc[:,"point_type"].isin(["H","L"]), "date"]
    df.set_index("date",inplace=True)
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
    'date':date_series,
    'article1': title1,
    'article2': title2,
    'article3': title3,
    'url1': url1,
    'url2': url2,
    'url3': url3,
    }
    df_time=pandas.DataFrame(frame)
    print(df_time)
