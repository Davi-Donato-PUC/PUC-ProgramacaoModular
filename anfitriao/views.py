from django.shortcuts import render, redirect
from anfitriao.anfitriao import *
from django.http import HttpResponse
from anfitriao.forms import *
from django.utils.timezone import now
from hotel.hotel import *

# Create your views here.

def anfitriaoView(request) :
    a = obterHoteisDoAnfitriao(request.session['anfitriao']['id'])
    hoteis = listarHoteisDoAnfitriao(a)
    return render(request,  'anfitriao.html', {'hoteis': hoteis , 'anfitriao': request.session['anfitriao'] })


def loginAnfitriaoView(request) :
    if request.method == "POST":
        formulario = AnfitriaoForm(request.POST)
        usuarios = ler_todos_anfitrioes()
        if formulario.is_valid() :
            nome = formulario.cleaned_data['nome']
            senha    = formulario.cleaned_data['senha']

            for usuario in usuarios:
                if usuario["nome"] == nome and usuario["senha"] == senha:
                    request.session["anfitriao"] = usuario
                    return redirect("/anfitriao/")  # nome da url restrita

        return HttpResponse("Usuário ou senha inválidos")

    formulario = AnfitriaoForm()
    return render(request,  'loginAnfitriao.html', { 'formulario': formulario, 'STATIC_VERSION': now().timestamp() })



def cadastroAnfitriaoView(request) :
    if request.method == 'POST' :
        formulario = AnfitriaoForm(request.POST)
        if formulario.is_valid() :
            nome = formulario.cleaned_data['nome']
            senha    = formulario.cleaned_data['senha']

            # verificado se username ja existe
            usuarios = ler_todos_anfitrioes()
            for usuario in usuarios:
                if usuario['nome'] == nome : return redirect('/cadastroAnfitriao')

            usuario = adicionar_anfitriao(nome, senha)
            request.session["anfitriao"] = usuario
            return redirect("/anfitriao/") 

    formulario = AnfitriaoForm()
    return render(request,  'cadastroAnfitriao.html', { 'formulario': formulario, 'STATIC_VERSION': now().timestamp() })



def adicionarHotelView(request) : 
    if request.method == 'POST' :
        formulario = HotelForm(request.POST)
        if formulario.is_valid() :
            nome = formulario.cleaned_data['nome']
            preco = formulario.cleaned_data['preco']
            descricao = formulario.cleaned_data['descricao']
            hotel_id = adicionarHotel(nome, preco, descricao)
            adicionarHotelAoAnfitriao(request.session["anfitriao"]['id'], hotel_id )
            formulario = HotelForm()
            return redirect('/anfitriao/')

    formulario = HotelForm()
    return render(request, 'adicionarHotel.html', { 'formulario': formulario,  })


def removerHotelView(reqeust) :
    pass
