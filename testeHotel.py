
from django.test import TestCase

# Create your tests here.
import unittest
import os
import json
from hotel.hotel import (
    ler_todos_hoteis, iniciarModulo, salvar_todos, obterHoteis,
    adicionarHotel, buscarHoteis, obterIdHoteisReservados,
    obterHoteisPorIds, obterReservasComDadosCompletos,
    buscar_hoteis_disponiveis, CAMINHO_ARQUIVO
)

# Dados simulados
DADOS_TESTE = [
    {"id": 1, "nome": "Hotel Luxo", "preco": "500", "descricao": "5 estrelas"},
    {"id": 2, "nome": "Hotel Simples", "preco": "200", "descricao": "2 estrelas"},
    {"id": 3, "nome": "Pousada Mar", "preco": "300", "descricao": "Vista para o mar"},
]

RESERVAS_TESTE = [
    {"usuario_id": 1, "hotel_id": 1, "checkin": "2025-07-01", "checkout": "2025-07-05"},
    {"usuario_id": 2, "hotel_id": 2, "checkin": "2025-07-10", "checkout": "2025-07-12"},
]

class TestModuloHotel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Garante um estado limpo antes dos testes
        cls.backup = None
        if os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, 'r') as f:
                cls.backup = f.read()

        with open(CAMINHO_ARQUIVO, 'w') as f:
            json.dump(DADOS_TESTE, f, indent=2)

        iniciarModulo()

    @classmethod
    def tearDownClass(cls):
        if cls.backup is not None:
            with open(CAMINHO_ARQUIVO, 'w') as f:
                f.write(cls.backup)

    def test_ler_todos_hoteis(self):
        hoteis = ler_todos_hoteis()
        self.assertIsInstance(hoteis, list)
        self.assertGreater(len(hoteis), 0)

    def test_salvar_todos_sucesso(self):
        resultado = salvar_todos(DADOS_TESTE)
        self.assertEqual(resultado, 0)

    def test_obter_hoteis(self):
        hoteis = obterHoteis()
        self.assertEqual(len(hoteis), len(DADOS_TESTE))

    def test_adicionar_hotel_valido(self):
        novo_id = adicionarHotel("Hotel Novo", "350", "Moderno")
        self.assertGreater(novo_id, 0)

    def test_adicionar_hotel_invalido(self):
        self.assertEqual(adicionarHotel("", "", ""), -1)

    def test_buscar_hoteis_nome_existente(self):
        resultado = buscarHoteis("luxo")
        self.assertEqual(len(resultado), 1)

    def test_buscar_hoteis_nome_inexistente(self):
        resultado = buscarHoteis("inexistente")
        self.assertEqual(resultado, [])

    def test_buscar_hoteis_criterio_invalido(self):
        resultado = buscarHoteis(12345)
        self.assertEqual(resultado, [])

    def test_obter_id_hoteis_reservados(self):
        ids = obterIdHoteisReservados(RESERVAS_TESTE)
        self.assertListEqual(ids, [1, 2])

    def test_obter_hoteis_por_ids(self):
        resultado = obterHoteisPorIds([1, 3])
        self.assertEqual(len(resultado), 2)
        ids_resultado = [h["id"] for h in resultado]
        self.assertIn(1, ids_resultado)
        self.assertIn(3, ids_resultado)

    def test_obter_reservas_com_dados_completos(self):
        resultado = obterReservasComDadosCompletos(RESERVAS_TESTE)
        self.assertEqual(len(resultado), 2)
        self.assertIn("checkin", resultado[0])
        self.assertIn("nome", resultado[0])

    def test_buscar_hoteis_disponiveis(self):
        # Função depende de obterReservas, então vamos injetar manualmente
        from reserva.reserva import obterReservas
        import types
        def fake_obterReservas():
            return RESERVAS_TESTE
        # Monkey patch
        original = obterReservas
        import reserva.reserva
        reserva.reserva.obterReservas = fake_obterReservas

        disponiveis = buscar_hoteis_disponiveis(1, DADOS_TESTE)
        self.assertEqual(len(disponiveis), 2)  # Hotel 1 já está reservado por user 1

        # Restaura original
        reserva.reserva.obterReservas = original

if __name__ == '__main__':
    unittest.main()
