import unittest
import os
import json
from anfitriao.anfitriao import (
    ler_todos_anfitrioes, salvar_anfitrioes, iniciarModuloAnfitriao,
    obterAnfitrioes, adicionar_anfitriao, listarHoteisDoAnfitriao,
    adicionarHotelAoAnfitriao, obterHoteisDoAnfitriao,
    CAMINHO_ARQUIVO
)

# Dados de teste
DADOS_TESTE = [
    {
        "id": 1,
        "nome": "Anfitriao1",
        "senha": "senha1",
        "hoteis_id": [10, 20]
    },
    {
        "id": 2,
        "nome": "Anfitriao2",
        "senha": "senha2",
        "hoteis_id": []
    }
]

# Mock para função obterHoteis (do módulo hotel)
def mock_obterHoteis():
    return [
        {"id": 10, "nome": "Hotel A", "preco": "100", "descricao": "desc A"},
        {"id": 20, "nome": "Hotel B", "preco": "200", "descricao": "desc B"},
        {"id": 30, "nome": "Hotel C", "preco": "300", "descricao": "desc C"},
    ]


class TestModuloAnfitriao(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.backup = None
        if os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, 'r', encoding='utf-8') as f:
                cls.backup = f.read()

        with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as f:
            json.dump(DADOS_TESTE, f, indent=4, ensure_ascii=False)

        iniciarModuloAnfitriao()

    @classmethod
    def tearDownClass(cls):
        if cls.backup is not None:
            with open(CAMINHO_ARQUIVO, 'w', encoding='utf-8') as f:
                f.write(cls.backup)

    def test_ler_todos_anfitrioes(self):
        anfitrioes = ler_todos_anfitrioes()
        self.assertIsInstance(anfitrioes, list)
        self.assertEqual(len(anfitrioes), len(DADOS_TESTE))

    def test_salvar_anfitrioes_sucesso(self):
        resultado = salvar_anfitrioes(DADOS_TESTE)
        self.assertEqual(resultado, 0)

    def test_obterAnfitrioes(self):
        anfitrioes = obterAnfitrioes()
        self.assertEqual(len(anfitrioes), len(DADOS_TESTE))

    def test_adicionar_anfitriao_valido(self):
        novo = adicionar_anfitriao("NovoAnfitriao", "novaSenha")
        self.assertIsInstance(novo, dict)
        self.assertEqual(novo["nome"], "NovoAnfitriao")
        self.assertEqual(novo["hoteis_id"], [])

    def test_adicionar_anfitriao_invalido(self):
        self.assertIsNone(adicionar_anfitriao("", ""))
        self.assertIsNone(adicionar_anfitriao("nome", ""))

    def test_listarHoteisDoAnfitriao(self):
        # Monkey patch obterHoteis para controlar retorno
        import anfitriao.anfitriao
        original = anfitriao.anfitriao.obterHoteis
        anfitriao.anfitriao.obterHoteis = mock_obterHoteis

        hoteis = listarHoteisDoAnfitriao([10, 30])
        self.assertEqual(len(hoteis), 2)
        ids = [h['id'] for h in hoteis]
        self.assertIn(10, ids)
        self.assertIn(30, ids)

        anfitriao.anfitriao.obterHoteis = original

    def test_adicionarHotelAoAnfitriao_sucesso(self):
        anfitriao_id = DADOS_TESTE[1]['id']  # Anfitriao2 sem hotéis
        resultado = adicionarHotelAoAnfitriao(anfitriao_id, 40)
        self.assertEqual(resultado, 1)
        # Verifica se o hotel foi adicionado
        ids_hoteis = obterHoteisDoAnfitriao(anfitriao_id)
        self.assertIn(40, ids_hoteis)

    def test_adicionarHotelAoAnfitriao_anfitriao_nao_encontrado(self):
        resultado = adicionarHotelAoAnfitriao(9999, 40)
        self.assertEqual(resultado, 0)

    def test_obterHoteisDoAnfitriao_existente(self):
        anfitriao_id = DADOS_TESTE[0]['id']  # Anfitriao1 tem 10 e 20
        hoteis = obterHoteisDoAnfitriao(anfitriao_id)
        self.assertListEqual(hoteis, [10, 20])

    def test_obterHoteisDoAnfitriao_inexistente(self):
        hoteis = obterHoteisDoAnfitriao(9999)
        self.assertEqual(hoteis, [])

if __name__ == "__main__":
    unittest.main()
