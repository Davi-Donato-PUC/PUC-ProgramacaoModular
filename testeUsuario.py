import unittest
import os
import json
from usuario.usuario import (
    ler_todos_usuarios, salvar_todos, iniciarModuloUsuario,
    obterUsuarios, adicionarUsuario, buscarUsuario, validarUsuario,
    CAMINHO_ARQUIVO
)

# Dados de teste
DADOS_TESTE = [
    {"id": 1, "username": "usuario1", "senha": "senha123"},
    {"id": 2, "username": "usuario2", "senha": "senha456"},
]

class TestModuloUsuario(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Faz backup do arquivo original (se existir)
        cls.backup = None
        if os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, 'r') as f:
                cls.backup = f.read()

        # Cria arquivo com dados de teste
        with open(CAMINHO_ARQUIVO, 'w') as f:
            json.dump(DADOS_TESTE, f, indent=2)

        iniciarModuloUsuario()

    @classmethod
    def tearDownClass(cls):
        # Restaura arquivo original após os testes
        if cls.backup is not None:
            with open(CAMINHO_ARQUIVO, 'w') as f:
                f.write(cls.backup)

    def test_ler_todos_usuarios(self):
        usuarios = ler_todos_usuarios()
        self.assertIsInstance(usuarios, list)
        self.assertEqual(len(usuarios), len(DADOS_TESTE))

    def test_salvar_todos_sucesso(self):
        resultado = salvar_todos(DADOS_TESTE)
        self.assertEqual(resultado, 0)

    def test_obterUsuarios(self):
        usuarios = obterUsuarios()
        self.assertEqual(len(usuarios), len(DADOS_TESTE))

    def test_adicionarUsuario_valido(self):
        novo_usuario = adicionarUsuario("novo_user", "nova_senha")
        self.assertIsInstance(novo_usuario, dict)
        self.assertEqual(novo_usuario["username"], "novo_user")

    def test_adicionarUsuario_invalido(self):
        self.assertIsNone(adicionarUsuario("", ""))
        self.assertIsNone(adicionarUsuario("user", ""))

    def test_buscarUsuario_por_id_existente(self):
        resultado = buscarUsuario(1)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["username"], "usuario1")

    def test_buscarUsuario_por_id_inexistente(self):
        resultado = buscarUsuario(999)
        self.assertEqual(resultado, [])

    def test_buscarUsuario_por_username_existente(self):
        resultado = buscarUsuario("usuario2")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 2)

    def test_buscarUsuario_por_username_inexistente(self):
        resultado = buscarUsuario("naoexiste")
        self.assertEqual(resultado, [])

    def test_buscarUsuario_criterio_invalido(self):
        resultado = buscarUsuario(12.34)
        self.assertEqual(resultado, [])

    def test_validarUsuario_senha_correta(self):
        resposta = validarUsuario("usuario1", "senha123")
        self.assertEqual(resposta, "Senha correta")

    def test_validarUsuario_senha_incorreta(self):
        resposta = validarUsuario("usuario1", "senha_errada")
        self.assertEqual(resposta, "Senha incorreta")

    def test_validarUsuario_usuario_nao_cadastrado(self):
        resposta = validarUsuario("usuarioX", "senha123")
        self.assertEqual(resposta, "Usuário não cadastrado")

if __name__ == "__main__":
    unittest.main()
