from django.shortcuts import render, redirect
from django.utils.timezone import now
from reserva.reserva import *
from hotel.hotel import *

def reservasView(request) :
    if 'usuario' not in request.session :
        return redirect('/login/')
    reservas = listar_reservas_por_usuario(request.session['usuario']['id'])
    ids = obterIdHoteisReservados(reservas)
    hoteis = obterHoteisPorIds(ids)

    usuario = request.session['usuario']
    return render(request, 'reservas.html', { 'usuario': usuario, 'hoteis' : hoteis , 'STATIC_VERSION': now().timestamp()  })


def adicionarReservaView(request, hotel_id) :
    usuario_id = request.session['usuario']['id']
    adicionarReserva(hotel_id, usuario_id)
    return redirect('/hoteis/')


def removerReservaView(request, hotel_id) :
    excluirReserva(hotel_id, request.session['usuario']['id'])
    return redirect('/reservas/')



 

 
