from django.contrib import admin
from django.urls import path
from hotel.views import hoteisView
from django.shortcuts import render, redirect


def noneRedirectView(request) :
    return redirect('hoteis/')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', noneRedirectView),
    path('hoteis/', hoteisView),
    path('hoteis/<str:pesquisa>', hoteisView),



]




