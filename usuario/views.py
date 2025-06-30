from django.shortcuts import render, redirect
from usuario.forms import LoginForm
from django.http import HttpResponse
from usuario.usuario import *
from django.utils.timezone import now

# Create your views here.

def cadastroView(request) :
    if request.method == 'POST' :
        formulario = LoginForm(request.POST)
        if formulario.is_valid() :
            username = formulario.cleaned_data['username']
            senha    = formulario.cleaned_data['senha']

            # verificado se username ja existe
            usuarios = ler_todos_usuarios()
            for usuario in usuarios:
                if usuario['username'] == username : return redirect('/cadastro')

            usuario = adicionarUsuario(username, senha)
            request.session["usuario"] = usuario
            return redirect("/hoteis/") 


    formulario = LoginForm()
    return render(request, 'cadastro.html', { 'formulario': formulario, 'STATIC_VERSION': now().timestamp() })


def loginView(request):
    if request.method == "POST":
        formulario = LoginForm(request.POST)
        usuarios = ler_todos_usuarios()
        if formulario.is_valid() :
            username = formulario.cleaned_data['username']
            senha    = formulario.cleaned_data['senha']

            for usuario in usuarios:
                if usuario["username"] == username and usuario["senha"] == senha:
                    request.session["usuario"] = usuario
                    return redirect("/hoteis/")  # nome da url restrita

        return HttpResponse("Usuário ou senha inválidos")
    formulario = LoginForm()
    return render(request, "login.html", { 'formulario': formulario, 'STATIC_VERSION': now().timestamp() })


def logoutView(request) :
    request.session.flush()
    return redirect("/loginAnfitriao/")
