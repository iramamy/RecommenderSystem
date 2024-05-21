from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    context = {
        'range_list': range(6),
        'range_list_1': range(12)
    }
    return render(request, 'home.html', context)