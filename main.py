import http.client, urllib.parse

import pandas

from stock_news import get_stock_news, get_peaks_and_troughs, set_df, clean_df, get_articels_dataframe_related_to_peaks
from api import  FinancialDataAPI



if __name__ == '__main__':
    findata = FinancialDataAPI()
    obj = findata.listing_EoDTimeseries(scheme="VALOR_BC", listings=["1222171_4"], from_date="2022-07-01")
    df = set_df(obj)
    df = clean_df(df)
    df.to_csv('stock_data.csv')
    df = get_articels_dataframe_related_to_peaks(df)