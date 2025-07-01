from django.apps import AppConfig
from anfitriao.anfitriao import iniciarModuloAnfitriao, salvar_anfitrioes, obterAnfitrioes
import atexit
import os


class AnfitriaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anfitriao'
    def ready(self):
        inicializar()



def inicializar():
    if os.environ.get('RUN_MAIN') == 'true':

        iniciarModuloAnfitriao()
        atexit.register(on_exit)



def on_exit():
    salvar_anfitrioes(obterAnfitrioes())
    print('FECHANDO ANFITRIOES')
