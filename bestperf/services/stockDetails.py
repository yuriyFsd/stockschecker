import requests
from bs4 import BeautifulSoup
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.timeseries import TimeSeries
from bestperf.services import screener
from bestperf.models import Sector, Screens, StockExchange, WatchCompanies, RelationToUser

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

# print(getStockFundaments('PLTR'))
# exit(0)
def getStockActualPrice(ticker):
    ts = TimeSeries(key='P7N1IT65A05V0V3B', output_format='json')
    data, meta_data = ts.get_quote_endpoint(symbol=ticker)
    print(data)

def updateWathListScreens():

    whatchList = WatchCompanies.objects.filter(relation_to_user__title='Watch') \
        .select_related('stock_exchange') \
        .values_list('ticker', 'stock_exchange__name', named=True)
    # whatchList = WatchCompanies.objects.filter(relation_to_user__title='Watch').values_list('ticker', 'stock_exchange_id' , flat=False)

    # whatchlistTickers = WatchCompanies.objects.filter(relation_to_user=RelationToUser.objects.get(title='Watch'))
    # print('')
    # print(whatchList)
    # print('')
    #return 'OK'
    screensDir = './bestperf/static/screens'
    driver = screener.initDriver()
    for tickerObject in whatchList:  
        # print('tickerObject:', tickerObject.stock_exchange__name)
        # continue
        ticker = tickerObject.ticker
        exchange = tickerObject.stock_exchange__name
        yahooFinScreenPath = screener.getYahooFinScreen(driver, ticker, screensDir)
        googleFinScreenPath = screener.getGoogleFinScreen(driver, ticker, exchange, screensDir)
        googleFinChartScreenPath = screener.getGoogleFinChartScreen(driver, ticker, exchange, screensDir)


        print(yahooFinScreenPath)

        WatchCompanies.objects.filter(ticker=ticker).update(
            screens=Screens.objects.update_or_create(
                fin_google_screen_path=googleFinScreenPath.replace('bestperf/', '../') if googleFinScreenPath else '',
                fin_yahoo_screen_path=yahooFinScreenPath.replace('bestperf/', '../') if yahooFinScreenPath else '',
                finchart_google_screen_path=googleFinChartScreenPath.replace('bestperf/', '../') if googleFinChartScreenPath else '',
            )[0]
        )

    screener.quitDriver(driver)

