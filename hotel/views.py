from django.shortcuts import render, redirect
from django.http import HttpResponse
from hotel.hotel import *
from django.utils.timezone import now
from reserva.reserva import *

import os
# Create your views here.

def hoteisView(request, pesquisa=None) :
    if 'usuario' not in request.session :
        return redirect('/login/')
    usuario = request.session['usuario']

    if pesquisa :
        resultados = buscarHoteis(pesquisa)
        resultados = buscar_hoteis_disponiveis(usuario['id'], resultados)
        return render(request, 'home.html', {'usuario': usuario, 'STATUS': 'OK', 'pesquisa':resultados, 'STATIC_VERSION': now().timestamp() })
    
    
    resultados = obterHoteis()
    resultados = buscar_hoteis_disponiveis(usuario['id'], resultados)
    return render(request, 'home.html', { 'usuario': usuario, 'STATUS': 'OK', 'pesquisa' : resultados, 'STATIC_VERSION': now().timestamp() } )










