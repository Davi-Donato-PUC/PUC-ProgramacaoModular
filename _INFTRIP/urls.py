from django.contrib import admin
from django.urls import path
from hotel.views import hoteisView
from usuario.views import cadastroView, loginView, logoutView
from reserva.views import reservasView, adicionarReservaView, removerReservaView
from django.shortcuts import render, redirect
from anfitriao.views import *

def noneRedirectView(request) :
    return redirect('hoteis/')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', noneRedirectView),
    path('cadastro/', cadastroView),
    path('login/', loginView),
    path('logout/', logoutView),
    path('hoteis/', hoteisView),
    path('hoteis/<str:pesquisa>', hoteisView),
    path('reservas/', reservasView),
    path('adicionarReserva/<int:hotel_id>', adicionarReservaView, name='adicionarReserva' ),
    path('removerReserva/<int:hotel_id>', removerReservaView,   name='removerReserva' ),

    path('anfitriao/', anfitriaoView ),
    path('loginAnfitriao/', loginAnfitriaoView ),
    path('cadastroAnfitriao/', cadastroAnfitriaoView ),
    path('adicionarHotel/', adicionarHotelView ),
    path('removerHotel/', removerHotelView ),



]




 