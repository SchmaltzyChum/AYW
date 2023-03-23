import http.client, urllib.parse
from stock_news import get_stock_news, get_peaks_and_troughs



if __name__ == '__main__':
    zigzag = get_peaks_and_troughs("VALOR_BC", ["1222171_4"], "2020-07-01", threshold=1)
    print(zigzag[0].date)
    pass

    ###Please do not use it. We only have 100 request per Month in single uese
    #get_stock_news('TSLA')
