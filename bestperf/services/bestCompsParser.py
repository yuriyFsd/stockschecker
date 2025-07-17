import importlib
import sys
import django
import os

#from tests import t1
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import ssl
import json
import screener

sys.path.append('E:/projects/2024/dev/python/stockschecker')  # Add project root to path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockschecker.settings')  # Replace with your settings module
django.setup()
#sys.path.insert(0, 'E:/projects/2024/dev/python/stockschecker/bestperf')
from bestperf.models import Bestperf, Sector, Screens, StockExchange
# importlib.reload(Bestperf)
#import models

# models.test()
# exit(0)

def getAnalystRating():
    url = 'https://www.tradingview.com/markets/stocks-usa/market-movers-best-performing/'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup('table')

    rows = tables[0].find_all('tr') #Assuming the first table contains the data we need
    companies = []
    for row in rows:
        comp = {}

        a_tags = row.find_all('a')
        td_tags = row.find_all('td')
        if not td_tags:
            continue
        
        comp['price'] = td_tags[2].text.strip()
        comp["analyst"] = td_tags[-1].text.strip()
        for a_tag in a_tags:
            aClass = " ".join(a_tag.get('class'))
            title = a_tag.get('title')
            if 'tickerName' in aClass:
                comp["title"] = title.strip()
            else:
                comp["sector"] = title.strip()
        companies.append(comp)

    return companies

def getTechRating():
    url = 'https://scanner.tradingview.com/america/scan?label-product=markets-screener'
    requestData = {
        "columns": [
            "name",
            "description",
            # "logoid",
            # "update_mode",
            # "type",
            # "typespecs",
            "Recommend.All",
            "Recommend.MA",
            "Recommend.Other",
            "RSI",
            # "Mom",
            # "pricescale",
            # "minmov",
            # "fractional",
            # "minmove2",
            # "AO",
            # "CCI20",
            # "Stoch.K",
            # "Stoch.D",
            # "MACD.macd",
            # "MACD.signal"
        ],
        "ignore_unknown_fields": False,
        "options": {
            "lang": "en"
        },
        "range": [
            0,
            100
        ],
        "sort": {
            "sortBy": "Perf.Y",
            "sortOrder": "desc",
            "nullsFirst": False
        },
        "preset": "best_performing"
    }

    json_data = json.dumps(requestData).encode('utf-8')
    req = urllib.request.Request(url, data=json_data)
    req.add_header('Content-Type', 'application/json')
    
    totalCount = 0
    companies = {}
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        jsonResult = json.loads(result)
        totalCount = jsonResult['totalCount']
        companies = jsonResult['data']

    if totalCount == 0:
        return []
    return companies

def filterTechRating(companies):
    filtered = [comp for comp in companies if comp['d'][2] > 0.5 and comp['d'][3] > 0.5 and comp['d'][4] > 0]
    return filtered

def filterAnalystRating(companies):
    filtered = [comp for comp in companies if comp['analyst'] == 'Strong buy']
    return filtered

filteredTechComps = filterTechRating(getTechRating())
filteredAnalystComps = filterAnalystRating(getAnalystRating())
print('Tech Companies:', len(filteredTechComps))
print('Analyst Companies:', len(filteredAnalystComps))

def populateDB(comp: dict, compTicker: str, screensDir: dict):
    sector_obj, created = Sector.objects.update_or_create(
        name=comp['sector'].strip(),
    )

    screens_obj, created = Screens.objects.update_or_create(
        fin_yahoo_screen_path=screensDir.get('yahoo', ''),
        fin_google_screen_path=screensDir.get('google_fin', ''),
        finchart_google_screen_path=screensDir.get('google_fin_chart', ''),
    )

    stockExchange, created = StockExchange.objects.update_or_create(
        name=comp['stock_exchange'].strip(),
    )

    bestperf, created = Bestperf.objects.update_or_create(
        ticker = compTicker,
        price = comp['price'],
        sector = sector_obj,
        stock_exchange = stockExchange,
        screens = screens_obj,
        defaults = {
            'name': name,
            'timestamp': django.utils.timezone.now(),
        }
    )

def getBestComps(techComps, analystComps):
    analystDict = {comp['title'].split(' ')[0].strip(): comp for comp in analystComps}
    bestComps = []
    for comp in techComps:
        stockExchange = comp['s'].split(':')[0]
        compDetails = comp['d'][0]
        if compDetails in analystDict:
            analystDict[compDetails]['stock_exchange'] = stockExchange
            bestComps.append(analystDict[compDetails])
    return bestComps

bestComps = getBestComps(filteredTechComps, filteredAnalystComps)

print('Best Companies:', len(bestComps))

browserDriver = screener.initDriver() if len(bestComps) > 0 else None
for comp in bestComps:
    # print(comp['title'], comp['sector'])
    compTicker = comp['title'].split(' ')[0].strip()
    name = comp['title'].split('−')[1].strip()
    print(compTicker, name)

    screensDir = './../static/screens'
    
    try:
        yahooFinScreenPath = screener.getYahooFinScreen(browserDriver, compTicker, screensDir)
        googleFinChartScreenPath = screener.getGoogleFinChartScreen(browserDriver, compTicker, comp['stock_exchange'], screensDir)
        googleFinScreenPath = screener.getGoogleFinScreen(browserDriver, compTicker, comp['stock_exchange'], screensDir)

        screensDir = {
            'yahoo': yahooFinScreenPath,
            'google_fin_chart': googleFinChartScreenPath,
            'google_fin': googleFinScreenPath
        }
        populateDB(comp, compTicker, screensDir)
    except Exception as e:
        print(f"Error processing {compTicker}: {e}")


screener.quitDriver(browserDriver)
# tickers = [comp['title'].split(' ')[0].strip() for comp in bestComps]
# screensPath = screener.getScreenshots(tickers[0:2], './../screens')
# print('Screenshots:', screensPath)

