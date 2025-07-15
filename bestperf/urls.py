from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.addNewStock, name='add_new_stock')
]