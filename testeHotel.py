import unittest
from unittest.mock import patch, mock_open
import json

import hotel.hotel as hotel_mod


class TestHotelModule(unittest.TestCase):

    def setUp(self):
        # Estado inicial do sistema para testes
        self.hoteis_exemplo = [
            {"id": 1, "nome": "Hotel A", "preco": 200.0, "descricao": "Luxo"},
            {"id": 2, "nome": "Hotel B", "preco": 150.0, "descricao": "Econômico"}
        ]
        hotel_mod.ESTRUTURA_HOTEIS = self.hoteis_exemplo.copy()

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "nome": "Hotel A", "preco": 200.0, "descricao": "Luxo"}]')
    def test_ler_todos_hoteis(self, mock_file):
        resultado = hotel_mod.ler_todos_hoteis()
        self.assertEqual(resultado[0]["nome"], "Hotel A")
        mock_file.assert_called_with(hotel_mod.CAMINHO_ARQUIVO, "r")

    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_todos(self, mock_file):
        status = hotel_mod.salvar_todos(self.hoteis_exemplo)
        self.assertEqual(status, 0)
        mock_file.assert_called_with(hotel_mod.CAMINHO_ARQUIVO, "w")
        handle = mock_file()
        handle.write.assert_called()

    def test_iniciarModulo(self):
        with patch("hotel.hotel.ler_todos_hoteis", return_value=self.hoteis_exemplo):
            hotel_mod.iniciarModulo()
            self.assertEqual(hotel_mod.ESTRUTURA_HOTEIS, self.hoteis_exemplo)

    def test_obterHoteis(self):
        resultado = hotel_mod.obterHoteis()
        self.assertEqual(resultado, self.hoteis_exemplo)

    def test_adicionarHotel_valido(self):
        novo_id = hotel_mod.adicionarHotel("Hotel C", 300, "Boutique")
        self.assertEqual(novo_id, 3)
        self.assertTrue(any(h["nome"] == "Hotel C" for h in hotel_mod.ESTRUTURA_HOTEIS))

    def test_adicionarHotel_invalido(self):
        self.assertEqual(hotel_mod.adicionarHotel("", 300, "Descrição"), -1)

    def test_buscarHoteis(self):
        resultado = hotel_mod.buscarHoteis("a")  # deve achar Hotel A
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["nome"], "Hotel A")

    def test_buscarHoteis_criterio_invalido(self):
        self.assertEqual(hotel_mod.buscarHoteis(123), [])

    def test_obterIdHoteisReservados(self):
        reservas = [{"hotel_id": 1}, {"hotel_id": 2}]
        ids = hotel_mod.obterIdHoteisReservados(reservas)
        self.assertEqual(ids, [1, 2])

    def test_obterHoteisPorIds(self):
        resultado = hotel_mod.obterHoteisPorIds([2])
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 2)

    def test_obterReservasComDadosCompletos(self):
        reservas = [{"hotel_id": 1, "checkin": "2025-07-01", "checkout": "2025-07-02"}]
        resultado = hotel_mod.obterReservasComDadosCompletos(reservas)
        self.assertEqual(len(resultado), 1)
        self.assertIn("checkin", resultado[0])
        self.assertEqual(resultado[0]["nome"], "Hotel A")

    @patch("hotel.hotel.obterReservas")
    def test_buscar_hoteis_disponiveis(self, mock_obterReservas):
        mock_obterReservas.return_value = [
            {"usuario_id": 10, "hotel_id": 1},
            {"usuario_id": 20, "hotel_id": 2}
        ]
        resultado = hotel_mod.buscar_hoteis_disponiveis(10, self.hoteis_exemplo)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 2)


if __name__ == "__main__":
    unittest.main()
