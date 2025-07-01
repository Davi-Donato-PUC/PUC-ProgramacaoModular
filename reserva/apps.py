from django.apps import AppConfig
from reserva.reserva import iniciarModuloReserva, salvar_todas_reservas, obterReservas
import atexit
import os

class ReservaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reserva'

    def ready(self):
        inicializar()



def inicializar():
    if os.environ.get('RUN_MAIN') == 'true':
        iniciarModuloReserva()
        atexit.register(on_exit)


def on_exit():
    salvar_todas_reservas(obterReservas())
    print('FECHANDO RESERVA')
