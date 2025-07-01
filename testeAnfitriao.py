import unittest
from unittest.mock import patch, mock_open
import json

import anfitriao.anfitriao as anfitriao_mod


class TestAnfitriaoModule(unittest.TestCase):

    def setUp(self):
        self.exemplo_anfitrioes = [
            {"id": 1, "nome": "Carlos", "senha": "1234", "hoteis_id": [1, 2]},
            {"id": 2, "nome": "Ana", "senha": "abcd", "hoteis_id": []}
        ]
        anfitriao_mod.ESTRUTURA_ANFITRIOES = self.exemplo_anfitrioes.copy()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "nome": "Carlos", "senha": "1234", "hoteis_id": [1]}
    ]))
    def test_ler_todos_anfitrioes_valido(self, mock_file, mock_exists):
        resultado = anfitriao_mod.ler_todos_anfitrioes()
        self.assertEqual(resultado[0]["nome"], "Carlos")

    @patch("os.path.exists", return_value=False)
    def test_ler_todos_anfitrioes_arquivo_inexistente(self, mock_exists):
        resultado = anfitriao_mod.ler_todos_anfitrioes()
        self.assertEqual(resultado, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_anfitrioes(self, mock_file):
        status = anfitriao_mod.salvar_anfitrioes(self.exemplo_anfitrioes)
        self.assertEqual(status, 0)
        mock_file.assert_called_with(anfitriao_mod.CAMINHO_ARQUIVO, "w", encoding="utf-8")

    def test_iniciarModuloAnfitriao(self):
        with patch("anfitriao.anfitriao.ler_todos_anfitrioes", return_value=self.exemplo_anfitrioes):
            anfitriao_mod.iniciarModuloAnfitriao()
            self.assertEqual(anfitriao_mod.ESTRUTURA_ANFITRIOES, self.exemplo_anfitrioes)

    def test_obterAnfitrioes(self):
        resultado = anfitriao_mod.obterAnfitrioes()
        self.assertEqual(resultado, self.exemplo_anfitrioes)

    def test_adicionar_anfitriao_valido(self):
        novo = anfitriao_mod.adicionar_anfitriao("Bruno", "senha123")
        self.assertIsInstance(novo, dict)
        self.assertEqual(novo["nome"], "Bruno")
        self.assertEqual(novo["id"], 3)

    def test_adicionar_anfitriao_invalido(self):
        self.assertIsNone(anfitriao_mod.adicionar_anfitriao("", ""))
        self.assertIsNone(anfitriao_mod.adicionar_anfitriao("Joao", ""))

    @patch("anfitriao.anfitriao.obterHoteis")
    def test_listarHoteisDoAnfitriao(self, mock_obterHoteis):
        mock_obterHoteis.return_value = [
            {"id": 1, "nome": "Hotel A"},
            {"id": 2, "nome": "Hotel B"},
            {"id": 3, "nome": "Hotel C"},
        ]
        resultado = anfitriao_mod.listarHoteisDoAnfitriao([1, 3])
        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0]["id"], 1)
        self.assertEqual(resultado[1]["id"], 3)

    def test_adicionarHotelAoAnfitriao_sucesso(self):
        status = anfitriao_mod.adicionarHotelAoAnfitriao(2, 5)
        self.assertEqual(status, 1)
        self.assertIn(5, anfitriao_mod.ESTRUTURA_ANFITRIOES[1]['hoteis_id'])

    def test_adicionarHotelAoAnfitriao_ja_existe(self):
        status = anfitriao_mod.adicionarHotelAoAnfitriao(1, 1)
        self.assertEqual(status, 1)  # Mesmo que já exista, retorna 1

    def test_adicionarHotelAoAnfitriao_inexistente(self):
        status = anfitriao_mod.adicionarHotelAoAnfitriao(999, 1)
        self.assertEqual(status, 0)

    def test_obterHoteisDoAnfitriao_valido(self):
        resultado = anfitriao_mod.obterHoteisDoAnfitriao(1)
        self.assertEqual(resultado, [1, 2])

    def test_obterHoteisDoAnfitriao_inexistente(self):
        resultado = anfitriao_mod.obterHoteisDoAnfitriao(999)
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()
