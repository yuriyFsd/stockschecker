import django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Bestperf
import bestperf.services.stockDetails as stockDetails
import bestperf.services.screener as screener
from bestperf.models import WatchCompanies, Sector, Screens, StockExchange, RelationToUser

# Create your views here.

def index(request):
    return render(request, "bestperformers/index.html", {
        'bestperformers': Bestperf.objects.all(),
        
    })

def watchList(request):
    return render(request, "bestperformers/watchlist.html", {
        'watchlist': WatchCompanies.objects.filter(relation_to_user__title='Watch'),
    })

def addNewStock(request):
    if request.method == 'POST':
        ticker = request.POST['ticker']
        fundamentals = stockDetails.getStockFundaments(ticker)
        if not fundamentals:
            return
        populateWatchlistDB(fundamentals, ticker)
        return render(request, "bestperformers/watchlist.html") #HttpResponseRedirect(reverse('bestperformers/watchlist.html'))


def getWatchListAllScreens(request):
    print('getWatchListAllScreens !!!!!!!!!!!!!!')
    stockDetails.updateWathListScreens()
    return render(request, "bestperformers/watchlist.html") 

def populateWatchlistDB(fundamentals: dict, ticker: str):
        """
        Populate the database with a new stock, given its fundamentals.

        Args:
            fundamentals (dict): A dictionary containing the stock's name, sector, exchange, etc.
            ticker (str): The stock's ticker symbol.

        Returns:
            None
        """
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
            relation_to_user = RelationToUser.objects.get(title='Watch'),
            defaults = {
                'name': fundamentals['name'],
                'timestamp': django.utils.timezone.now(),
            }
        )
