from django.shortcuts import render, redirect
from django.http import HttpResponse
from hotel.hotel import *
import os
# Create your views here.

def hoteisView(request, pesquisa=None) :
    if pesquisa :
        resultados = buscarHotel(pesquisa)

        return render(request, 'home.html', {'STATUS': 'OK', 'pesquisa':resultados })
    
    #adicionarHotel('Copacabana Palace', '500', 'BLABLABLA')
    return render(request, 'home.html', {'STATUS': 'OK', 'pesquisa' : []} )










