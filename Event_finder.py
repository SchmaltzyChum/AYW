"""
Example of how to get news related to peaks of the stock of SIX.

We use the API from marketaux to get the stock news.
More information: https://www.marketaux.com/documentation

The free API version, which is limited to 100 request per day.
"""
from stock_news import set_df, clean_df, get_articles_dataframe_related_to_peaks
from api import  FinancialDataAPI


if __name__ == '__main__':

    #Connect to the Financial Api to get Stock Data
    findata = FinancialDataAPI()

    #Specifiy which Data you want
    obj = findata.listing_EoDTimeseries(scheme="VALOR_BC", listings=["1222171_4"], from_date="2022-07-01")

    #Create dataframe from the financial data
    df = set_df(obj)
    df = clean_df(df)

    #Get dataframe of the artciles which a related to the peaks and trough
    #The token currently using the free API version, which is limited to 100 request per day
    df_peaks_and_trough = get_articles_dataframe_related_to_peaks(df, token="7PF9IeuR79wUE8rw2skJVsjJFErB6I1O093q7iWI")

    #optional: show the data frame
    print(df_peaks_and_trough)
