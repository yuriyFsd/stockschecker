from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('addnewstock', views.addNewStock, name='add_new_stock'),
    path('watchlist', views.watchList, name='watchlist'),
    path('getwatchlistallscreens', views.getWatchListAllScreens, name='getwatchlistallscreens'),
    path('update_item_screens/<int:pk>', views.update_item_screens, name='update_item_screens'),
    path('show_item/<int:pk>', views.show_item, name='show_item'),
    path('delete_item/<int:pk>', views.delete_item, name='delete_item'),
]