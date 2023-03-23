import http.client, urllib.parse
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
    #print(s)
    #print(get_stock_news('SIX', )
