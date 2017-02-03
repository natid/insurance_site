from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def nir(request):
    return HttpResponse('<h1>Nir!!!</h1>')
