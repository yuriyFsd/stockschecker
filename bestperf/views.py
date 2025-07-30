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
        'watchlist': WatchCompanies.objects.filter(relation_to_user__title='Watch', removed=False),
        'list_title': 'Watch Companies',
    })
 
def owned(request):
    return render(request, "bestperformers/watchlist.html", {
        'watchlist': WatchCompanies.objects.filter(relation_to_user__title='Own', removed=False),
        'list_title': 'Owned Companies',
    })


def addNewStock(request):
    if request.method == 'POST':
        ticker = request.POST['ticker'].upper().strip()
        sourcePage = request.META.get('HTTP_REFERER')
        if 'watchlist' in sourcePage:
            sourcePage = 'watchlist'
        elif 'owned' in sourcePage:
            sourcePage = 'owned'

        print(f"SOURCE: {sourcePage}")

        ifStockInDB = WatchCompanies.objects.filter(ticker=ticker).exists()
        if ifStockInDB:
            WatchCompanies.objects.filter(ticker=ticker).update(removed=False)
            return render(request, "bestperformers/watchlist.html")

        fundamentals = stockDetails.getStockFundaments(ticker)
        # print('fundamentals: ', fundamentals)
        if not fundamentals:
            return
        populateWatchlistDB(fundamentals, ticker, sourcePage)
        if sourcePage == 'watchlist':
            return HttpResponseRedirect(reverse('watchlist'))
        elif sourcePage == 'owned':                
            return HttpResponseRedirect(reverse('owned'))
        
        return render(request, "bestperformers/watchlist.html")

def getWatchListAllScreens(request):
    sourcePage = request.META.get('HTTP_REFERER')
    sourcePage = 'owned' if 'owned' in sourcePage else 'watchlist'
    stockDetails.updateWatchListScreens(sourcePage)
    return render(request, "bestperformers/watchlist.html") 

def populateWatchlistDB(fundamentals: dict, ticker: str, sourcePage: str):
    relationToUserValue = 'Own' if sourcePage == 'owned' else'Watch'
    print('RELATION!!!: ', relationToUserValue,  RelationToUser.objects.get(title=relationToUserValue))
    sector_obj, created = Sector.objects.update_or_create(
        name=fundamentals['sector'].strip(),
    )
    stockExchange, created = StockExchange.objects.update_or_create(
        name=fundamentals['exchange'].strip(),
    )
    watchCompany, created = WatchCompanies.objects.update_or_create(
        ticker = ticker,
        defaults = {
            'name': fundamentals['name'],
            'price': '',
            'sector': sector_obj,
            'stock_exchange': stockExchange,
            'relation_to_user': RelationToUser.objects.get(title=relationToUserValue),
            'timestamp': django.utils.timezone.now(),
        }
    )

def delete_item(request, pk):
    WatchCompanies.objects.filter(pk=pk).update(removed=True)
    # WatchCompanies.objects.filter(pk=pk).delete()

    return HttpResponseRedirect(reverse('watchlist'))
    return render(request, "bestperformers/watchlist.html")

    # return HttpResponseRedirect(reverse('bestperformers/watchlist.html'))

def update_item_screens(request, pk):
    stockDetails.updateItemScreens(pk)
    return HttpResponseRedirect(reverse('watchlist'))
    return render(request, "bestperformers/watchlist.html")

def update_exchange_title(request, pk):
    WatchCompanies.objects.filter(pk=pk).update(stock_exchange=StockExchange.objects.get(pk=request.POST['exchange_title']))
    return HttpResponseRedirect(reverse('watchlist'))
    return render(request, "bestperformers/item.html")

def show_item(request, pk):
    stock = WatchCompanies.objects.get(pk=pk)
    return render(request, "bestperformers/item.html", {
        'stock_details': stock,
    })
