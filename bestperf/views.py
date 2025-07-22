import django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Bestperf
import bestperf.services.stockDetails as stockDetails
import bestperf.services.screener as screener
from bestperf.models import WatchCompanies, Sector, Screens, StockExchange

# Create your views here.

def index(request):
    return render(request, "bestperformers/index.html", {
        'bestperformers': Bestperf.objects.all(),
        
    })

def watchList(request):
    return render(request, "bestperformers/watchlist.html", {
    })

def addNewStock(request):
    if request.method == 'POST':
        #get fundamentals
        ticker = request.POST['ticker']
        fundamentals = stockDetails.getStockFundaments(ticker)
        print(1111111111111)
        print(fundamentals)
        sector_obj, created = Sector.objects.update_or_create(
            name=fundamentals['sector'].strip(),
        )

        stockExchange, created = StockExchange.objects.update_or_create(
            name=fundamentals['exchange'].strip(),
        )
        
        watchCompany, created = WatchCompanies.objects.update_or_create(
            ticker = ticker,
            price = '',
            sector = sector_obj,
            stock_exchange = stockExchange,
            defaults = {
                'name': fundamentals['name'],
                'timestamp': django.utils.timezone.now(),
            }
        )
        #show to watch list
        #make button "get all screens"

        # ticker = str(request.POST['ticker'])
        # print(ticker)
        # driver = screener.initDriver()
        # screensDir = './bestperf/static/screens'
        # patch = screener.getYahooFinScreen(driver, ticker, screensDir)
        # print(patch)
        # screener.quitDriver(driver)
        # return
        # bestperf = Bestperf.objects.create(
        #     ticker=ticker
        # )
        return render(request, "bestperformers/watchlist.html") #HttpResponseRedirect(reverse('bestperformers/watchlist.html'))
        

# def populateDB(comp: dict, compTicker: str, screensDir: dict):
#     sector_obj, created = Sector.objects.update_or_create(
#         name=comp['sector'].strip(),
#     )

#     screens_obj, created = Screens.objects.update_or_create(
#         fin_yahoo_screen_path=screensDir.get('yahoo', ''),
#         fin_google_screen_path=screensDir.get('google_fin', ''),
#         finchart_google_screen_path=screensDir.get('google_fin_chart', ''),
#     )

#     stockExchange, created = StockExchange.objects.update_or_create(
#         name=comp['stock_exchange'].strip(),
#     )

#     bestperf, created = Bestperf.objects.update_or_create(
#         ticker =  ticker,
#         price = '',
#         sector = sector_obj,
#         stock_exchange = stockExchange,
#         defaults = {
#             'name': name,
#             'timestamp': django.utils.timezone.now(),
#         }
#     )
