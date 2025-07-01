from django.apps import AppConfig
from usuario.usuario import iniciarModuloUsuario, salvar_todos, obterUsuarios
import os

import atexit

class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuario'
    
    def ready(self):
        inicializar()



def inicializar():
    if os.environ.get('RUN_MAIN') == 'true':
        iniciarModuloUsuario()
        atexit.register(on_exit)


def on_exit():
    salvar_todos(obterUsuarios())
    print('FECHANDO CLIENTES')


