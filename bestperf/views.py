from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Bestperf

# Create your views here.

def index(request):
    return render(request, "bestperformers/index.html", {
        'bestperformers': Bestperf.objects.all(),
        
    })

def addNewStock(request):
    if request.method == 'POST':

        ticker = str(request.POST['ticker'])
        bestperf = Bestperf.objects.create(
            ticker=ticker
        )
        return HttpResponseRedirect(reverse('index'))
        