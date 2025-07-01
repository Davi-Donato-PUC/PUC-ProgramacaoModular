import unittest
import os
import json
from reserva.reserva import (
    ler_todas_reservas, salvar_todas_reservas, iniciarModuloReserva,
    obterReservas, adicionarReserva, excluirReserva,
    listar_reservas_por_usuario, CAMINHO_ARQUIVO
)

# Dados de teste para o arquivo JSON de reservas
DADOS_TESTE = [
    {
        "id": 1,
        "hotel_id": 10,
        "usuario_id": 100,
        "checkin": "2025-07-01",
        "checkout": "2025-07-05"
    },
    {
        "id": 2,
        "hotel_id": 20,
        "usuario_id": 200,
        "checkin": "2025-07-10",
        "checkout": "2025-07-15"
    }
]

class TestModuloReserva(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Backup do arquivo original (se existir)
        cls.backup = None
        if os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, 'r') as f:
                cls.backup = f.read()

        # Cria arquivo com dados de teste
        with open(CAMINHO_ARQUIVO, 'w') as f:
            json.dump(DADOS_TESTE, f, indent=2)

        iniciarModuloReserva()

    @classmethod
    def tearDownClass(cls):
        # Restaura arquivo original após testes
        if cls.backup is not None:
            with open(CAMINHO_ARQUIVO, 'w') as f:
                f.write(cls.backup)

    def test_ler_todas_reservas(self):
        reservas = ler_todas_reservas()
        self.assertIsInstance(reservas, list)
        self.assertEqual(len(reservas), len(DADOS_TESTE))

    def test_salvar_todas_reservas_sucesso(self):
        resultado = salvar_todas_reservas(DADOS_TESTE)
        self.assertEqual(resultado, 0)

    def test_obterReservas(self):
        reservas = obterReservas()
        self.assertEqual(len(reservas), len(DADOS_TESTE))

    def test_adicionarReserva_sucesso(self):
        # Hotel 30 não está reservado
        novo_id = adicionarReserva(30, 300, "2025-08-01", "2025-08-05")
        self.assertIsInstance(novo_id, int)
        self.assertGreater(novo_id, 0)

    def test_adicionarReserva_erro_dados_incompletos(self):
        resultado = adicionarReserva(None, 300, "2025-08-01", "2025-08-05")
        self.assertEqual(resultado, -1)

    def test_adicionarReserva_ja_reservado(self):
        # Hotel 10 já está reservado em DADOS_TESTE
        resultado = adicionarReserva(10, 999, "2025-08-01", "2025-08-05")
        self.assertEqual(resultado, 0)

    def test_excluirReserva_sucesso(self):
        # Primeiro adiciona reserva para excluir
        adicionarReserva(40, 400, "2025-09-01", "2025-09-05")
        resultado = excluirReserva(40, 400)
        self.assertEqual(resultado, 1)

    def test_excluirReserva_nao_encontrado(self):
        resultado = excluirReserva(999, 999)
        self.assertEqual(resultado, 0)

    def test_listar_reservas_por_usuario(self):
        # Usuário 100 tem 1 reserva no DADOS_TESTE
        resultado = listar_reservas_por_usuario(100)
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 1)

    def test_listar_reservas_por_usuario_sem_reservas(self):
        resultado = listar_reservas_por_usuario(9999)
        self.assertEqual(resultado, [])

if __name__ == "__main__":
    unittest.main()
