import unittest
from unittest.mock import patch, mock_open
import json

import usuario.usuario as usuario_mod


class TestUsuarioModule(unittest.TestCase):

    def setUp(self):
        self.usuarios_exemplo = [
            {"id": 1, "username": "alice", "senha": "123"},
            {"id": 2, "username": "bob", "senha": "456"}
        ]
        usuario_mod.ESTRUTURA_USUARIOS = self.usuarios_exemplo.copy()

    # --- ler_todos_usuarios ---
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "username": "alice", "senha": "123"}
    ]))
    def test_ler_todos_usuarios_sucesso(self, mock_file):
        resultado = usuario_mod.ler_todos_usuarios()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["username"], "alice")
        mock_file.assert_called_with(usuario_mod.CAMINHO_ARQUIVO, "r")

    @patch("builtins.open", side_effect=Exception("Erro ao ler"))
    def test_ler_todos_usuarios_erro(self, mock_file):
        resultado = usuario_mod.ler_todos_usuarios()
        self.assertEqual(resultado, [])

    # --- salvar_todos ---
    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_todos_sucesso(self, mock_file):
        status = usuario_mod.salvar_todos(self.usuarios_exemplo)
        self.assertEqual(status, 0)

    @patch("builtins.open", side_effect=Exception("Falha"))
    def test_salvar_todos_falha(self, mock_file):
        status = usuario_mod.salvar_todos(self.usuarios_exemplo)
        self.assertEqual(status, 1)

    # --- iniciarModuloUsuario ---
    def test_iniciarModuloUsuario(self):
        with patch("usuario.usuario.ler_todos_usuarios", return_value=self.usuarios_exemplo):
            usuario_mod.iniciarModuloUsuario()
            self.assertEqual(usuario_mod.ESTRUTURA_USUARIOS, self.usuarios_exemplo)

    # --- obterUsuarios ---
    def test_obterUsuarios(self):
        resultado = usuario_mod.obterUsuarios()
        self.assertEqual(resultado, self.usuarios_exemplo)

    # --- adicionarUsuario ---
    def test_adicionarUsuario_valido(self):
        novo = usuario_mod.adicionarUsuario("charlie", "789")
        self.assertIsInstance(novo, dict)
        self.assertEqual(novo["id"], 3)
        self.assertEqual(novo["username"], "charlie")

    def test_adicionarUsuario_invalido(self):
        self.assertIsNone(usuario_mod.adicionarUsuario("", "123"))
        self.assertIsNone(usuario_mod.adicionarUsuario("lucas", ""))

    # --- buscarUsuario ---
    def test_buscarUsuario_por_id(self):
        resultado = usuario_mod.buscarUsuario(1)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["username"], "alice")

    def test_buscarUsuario_por_username(self):
        resultado = usuario_mod.buscarUsuario("Bob")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 2)

    def test_buscarUsuario_criterio_invalido(self):
        resultado = usuario_mod.buscarUsuario(3.14)
        self.assertEqual(resultado, [])

    # --- validarUsuario ---
    def test_validarUsuario_correto(self):
        resultado = usuario_mod.validarUsuario("alice", "123")
        self.assertEqual(resultado, "Senha correta")

    def test_validarUsuario_senha_errada(self):
        resultado = usuario_mod.validarUsuario("bob", "errada")
        self.assertEqual(resultado, "Senha incorreta")

    def test_validarUsuario_nao_cadastrado(self):
        resultado = usuario_mod.validarUsuario("nao_existe", "123")
        self.assertEqual(resultado, "Usuário não cadastrado")


if __name__ == "__main__":
    unittest.main()
