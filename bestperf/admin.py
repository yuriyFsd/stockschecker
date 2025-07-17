from django.contrib import admin

from .models import Bestperf, Sector, StockExchange, Screens

# Register your models here.
admin.site.register(Bestperf)
admin.site.register(Sector)
admin.site.register(StockExchange)
admin.site.register(Screens)
