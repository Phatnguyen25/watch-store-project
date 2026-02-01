from django.shortcuts import render
from store.models import Store

def store_locator(request):
    return render(request, 'store/stores/locator.html')