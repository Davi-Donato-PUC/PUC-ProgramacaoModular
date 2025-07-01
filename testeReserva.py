import unittest
from unittest.mock import patch, mock_open
import json

import reserva.reserva as reserva_mod


class TestReservaModule(unittest.TestCase):

    def setUp(self):
        self.reservas_exemplo = [
            {"id": 1, "hotel_id": 10, "usuario_id": 101, "checkin": "2025-07-01", "checkout": "2025-07-03"},
            {"id": 2, "hotel_id": 20, "usuario_id": 102, "checkin": "2025-07-05", "checkout": "2025-07-06"}
        ]
        reserva_mod.ESTRUTURA_RESERVAS = self.reservas_exemplo.copy()

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps([
        {"id": 1, "hotel_id": 10, "usuario_id": 101, "checkin": "2025-07-01", "checkout": "2025-07-03"}
    ]))
    def test_ler_todas_reservas_valido(self, mock_file):
        resultado = reserva_mod.ler_todas_reservas()
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["hotel_id"], 10)
        mock_file.assert_called_with(reserva_mod.CAMINHO_ARQUIVO, "r")

    @patch("builtins.open", side_effect=Exception("Erro ao abrir"))
    def test_ler_todas_reservas_erro(self, mock_file):
        resultado = reserva_mod.ler_todas_reservas()
        self.assertEqual(resultado, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_salvar_todas_reservas(self, mock_file):
        status = reserva_mod.salvar_todas_reservas(self.reservas_exemplo)
        self.assertEqual(status, 0)
        handle = mock_file()
        handle.write.assert_called()

    def test_iniciarModuloReserva(self):
        with patch("reserva.reserva.ler_todas_reservas", return_value=self.reservas_exemplo):
            reserva_mod.iniciarModuloReserva()
            self.assertEqual(reserva_mod.ESTRUTURA_RESERVAS, self.reservas_exemplo)

    def test_obterReservas(self):
        resultado = reserva_mod.obterReservas()
        self.assertEqual(resultado, self.reservas_exemplo)

    def test_adicionarReserva_valida(self):
        novo_id = reserva_mod.adicionarReserva(30, 103, "2025-08-01", "2025-08-05")
        self.assertEqual(novo_id, 3)
        self.assertEqual(reserva_mod.ESTRUTURA_RESERVAS[-1]["hotel_id"], 30)

    def test_adicionarReserva_dados_incompletos(self):
        resultado = reserva_mod.adicionarReserva(None, 103, "2025-08-01", "2025-08-05")
        self.assertEqual(resultado, -1)

    def test_adicionarReserva_ja_reservado(self):
        resultado = reserva_mod.adicionarReserva(10, 104, "2025-08-10", "2025-08-12")
        self.assertEqual(resultado, 0)

    def test_excluirReserva_sucesso(self):
        status = reserva_mod.excluirReserva(10, 101)
        self.assertEqual(status, 1)
        self.assertFalse(any(r for r in reserva_mod.ESTRUTURA_RESERVAS if r["hotel_id"] == 10 and r["usuario_id"] == 101))

    def test_excluirReserva_nao_encontrada(self):
        status = reserva_mod.excluirReserva(999, 999)
        self.assertEqual(status, 0)

    def test_listar_reservas_por_usuario_existente(self):
        resultado = reserva_mod.listar_reservas_por_usuario(102)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["id"], 2)

    def test_listar_reservas_por_usuario_inexistente(self):
        resultado = reserva_mod.listar_reservas_por_usuario(999)
        self.assertEqual(resultado, [])


if __name__ == "__main__":
    unittest.main()
