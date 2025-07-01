from django.apps import AppConfig
from hotel.hotel import iniciarModulo, obterHoteis, salvar_todos
import atexit
import os


class HotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel'

    def ready(self):
        inicializar()



def inicializar():
    if os.environ.get('RUN_MAIN') == 'true':

        iniciarModulo()
        atexit.register(on_exit)



def on_exit():
    salvar_todos(obterHoteis())
    print('FECHANDO HOTEIS')


