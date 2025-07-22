from django.db import models


# def test():
#     print("This is a test function in models.py")


# Create your models here.
class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StockExchange(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Screens(models.Model):
    fin_yahoo_screen_path = models.CharField(max_length=500, blank=True, null=True)
    fin_google_screen_path = models.CharField(max_length=500, blank=True, null=True)
    finchart_google_screen_path = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.id)} | {self.fin_yahoo_screen_path} | {self.fin_google_screen_path} | {self.finchart_google_screen_path} | | {self.timestamp}"

class Bestperf(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=300, blank=True, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='best_perfs', blank=True, null=True)
    stock_exchange = models.ForeignKey(StockExchange, on_delete=models.CASCADE, related_name='best_perfs', blank=True, null=True)
    screens = models.ForeignKey(Screens, on_delete=models.CASCADE, related_name='best_perfs', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.ticker}:{self.stock_exchange}  {self.price}  {self.name} | {self.sector} | {self.screens} | {self.timestamp}"

class RelationToUser(models.Model):
    title = models.CharField(max_length=100) #own, watch

    def __str__(self):
        return f"{self.title}"

class WatchCompanies(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=300, blank=True, null=True)
    price = models.CharField(max_length=10, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='watch_list', blank=True, null=True)
    stock_exchange = models.ForeignKey(StockExchange, on_delete=models.CASCADE, related_name='watch_list', blank=True, null=True)
    screens = models.ForeignKey(Screens, on_delete=models.CASCADE, related_name='watch_list', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    relation_to_user = models.ForeignKey(RelationToUser, on_delete=models.CASCADE, related_name='watch_list', blank=True, null=True)

    def __str__(self):
        return f"{self.ticker}:{self.stock_exchange}  {self.price}  {self.name} | {self.sector} | {self.screens} | {self.timestamp}"
