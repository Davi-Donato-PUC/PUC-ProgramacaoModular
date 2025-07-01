from django.shortcuts import render, redirect
from django.utils.timezone import now
from reserva.reserva import *
from hotel.hotel import *
from datetime import datetime

def reservasView(request) :
    if 'usuario' not in request.session :
        return redirect('/login/')
    
    reservas = listar_reservas_por_usuario(request.session['usuario']['id'])
    #ids = obterIdHoteisReservados(reservas)
    #hoteis = obterHoteisPorIds(ids)
    hoteis = obterReservasComDadosCompletos(reservas)


    usuario = request.session['usuario']
    return render(request, 'reservas.html', { 'usuario': usuario, 'hoteis' : hoteis , 'STATIC_VERSION': now().timestamp()  })



def adicionarReservaView(request, hotel_id) :

    checkin_str = request.POST.get('checkin')
    checkout_str = request.POST.get('checkout')
    print(checkin_str)

    usuario_id = request.session['usuario']['id']
    adicionarReserva(hotel_id, usuario_id, checkin_str, checkout_str)
    return redirect('/hoteis/')


def removerReservaView(request, hotel_id) :
    excluirReserva(hotel_id, request.session['usuario']['id'])
    return redirect('/reservas/')



 

 
