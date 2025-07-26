import django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Bestperf
import bestperf.services.stockDetails as stockDetails
# import bestperf.services.screener as screener
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
        print('fundamentals: ', fundamentals)
        if not fundamentals:
            return
        populateWatchlistDB(fundamentals, ticker)
        return render(request, "bestperformers/watchlist.html") #HttpResponseRedirect(reverse('bestperformers/watchlist.html'))

def getWatchListAllScreens(request):
    stockDetails.updateWathListScreens()
    return render(request, "bestperformers/watchlist.html") 

def populateWatchlistDB(fundamentals: dict, ticker: str):
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

def delete_item(request, pk):
    WatchCompanies.objects.filter(pk=pk).delete()

    return HttpResponseRedirect(reverse('watchlist'))
    return render(request, "bestperformers/watchlist.html")

    # return HttpResponseRedirect(reverse('bestperformers/watchlist.html'))

def update_item_screens(request, pk):
    stockDetails.updateItemScreens(pk)
    return HttpResponseRedirect(reverse('watchlist'))
    return render(request, "bestperformers/watchlist.html")

def show_item(request, pk):
    stock = WatchCompanies.objects.get(pk=pk)
    return render(request, "bestperformers/item.html", {
        'stock_details': stock,
    })
