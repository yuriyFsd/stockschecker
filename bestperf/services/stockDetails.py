import requests
from bs4 import BeautifulSoup
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries

def getStockFundaments(ticker):
    fd = FundamentalData(key='P7N1IT65A05V0V3B', output_format='json')
    data, meta_data = fd.get_company_overview(symbol=ticker)
    print(data)
    return {
        'name': data.get('Name'),
        'sector': data.get('Sector'),
        'exchange': data.get('Exchange'),
        'industry': data.get('Industry'),
        # 'marketCapitalization': data.get('MarketCapitalization')  # Note: actual price may need a different endpoint
    }

def getStockActualPrice(ticker):
    ts = TimeSeries(key='P7N1IT65A05V0V3B', output_format='json')
    data, meta_data = ts.get_quote_endpoint(symbol=ticker)
    print(data)

# print(getStockFundaments('IREN'))
# getStockActualPrice('IREN')

# def parseStockDetails(ticker = 'IREN'):
#     url = f"https://finviz.com/quote.ashx?t={ticker}&p=d"
#     html = requests.get(url).text
#     print(html)
#     soup = BeautifulSoup(html, 'html.parser')
#     print(getStockName(soup))
#     return soup

# def getStockName(soup):
#     tag = soup.find('a', class_='tab-link block truncate')
#     if tag is None:
#         return None
#     return tag.text



# https://finviz.com/quote.ashx?t=IREN&p=d