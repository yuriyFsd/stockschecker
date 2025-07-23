from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('addnewstock', views.addNewStock, name='add_new_stock'),
    path('watchlist', views.watchList, name='watchlist'),
    path('getwatchlistallscreens', views.getWatchListAllScreens, name='getwatchlistallscreens'),
]