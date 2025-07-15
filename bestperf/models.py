from django.db import models


# def test():
#     print("This is a test function in models.py")


# Create your models here.
class Sector(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Bestperf(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='best_perfs', blank=True, null=True)
    fin_yahoo_screen_path = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticker}: {self.name} | ({self.sector})"
