import json
from datetime import datetime
import atexit

import json

CAMINHO_ARQUIVO = "reserva/dadosReserva.json"

# ======================
# Função: ler_todas_reservas
# ======================
# Descrição:
# Lê todas as reservas salvas no arquivo JSON. Retorna lista de reservas ou [] em caso de erro.
# Acoplamento:
# - Depende da existência do arquivo definido por CAMINHO_ARQUIVO.
# Hipóteses:
# - O arquivo existe e possui uma estrutura de lista de dicionários.
# Interface com o Usuário:
# - Apenas imprime mensagens em caso de erro.

def ler_todas_reservas():
    try:
        with open(CAMINHO_ARQUIVO, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRO] Falha ao ler reservas: {e}")
        return []


# ======================
# Função: salvar_todas_reservas
# ======================
# Descrição:
# Salva a lista de reservas no arquivo JSON.
# Retornos:
# - 0: sucesso
# - 1: erro ao salvar
def salvar_todas_reservas(dados):
    try:
        with open(CAMINHO_ARQUIVO, "w") as f:
            json.dump(dados, f, indent=2)
        return 0
    except Exception as e:
        print(f"[ERRO] Falha ao salvar reservas: {e}")
        return 1


# ======================
# Função: iniciarModuloReserva
# ======================
# Descrição:
# Inicializa o módulo de reservas carregando os dados em memória.
# Interface com o Usuário:
# - Exibe mensagem de inicialização.
def iniciarModuloReserva():
    global ESTRUTURA_RESERVAS
    ESTRUTURA_RESERVAS = ler_todas_reservas()
    print('INICIADO RESERVAS')


# ======================
# Função: obterReservas
# ======================
# Descrição:
# Retorna a estrutura de reservas atualmente carregada em memória.
def obterReservas():
    global ESTRUTURA_RESERVAS
    return ESTRUTURA_RESERVAS


# ======================
# Função: adicionarReserva
# ======================
# Descrição:
# Adiciona uma nova reserva se ainda não existir uma reserva para o mesmo hotel.
# Acoplamento:
# - Depende da estrutura ESTRUTURA_RESERVAS já estar carregada.
# Retornos:
# - 0: reserva já existe para o hotel
# - ID: da nova reserva criada
# - -1: erro nos dados
def adicionarReserva(hotelId, usuarioId, checkin, checkout):
    global ESTRUTURA_RESERVAS

    if not all([hotelId, usuarioId, checkin, checkout]):
        return -1  # Dados incompletos

    dados = ESTRUTURA_RESERVAS
    novo_id = 1 if not dados else max(item["id"] for item in dados) + 1

    for dado in dados:
        if hotelId == dado['hotel_id']:
            return 0  # Já reservado

    novo = {
        "id": novo_id,
        "hotel_id": hotelId,
        "usuario_id": usuarioId,
        "checkin": checkin,
        "checkout": checkout
    }

    dados.append(novo)
    return novo_id


# ======================
# Função: excluirReserva
# ======================
# Descrição:
# Remove a reserva do usuário em um determinado hotel.
# Retornos:
# - 0: nenhuma reserva encontrada
# - 1: reserva removida com sucesso
def excluirReserva(hotelId, usuarioId):
    global ESTRUTURA_RESERVAS
    lista = ESTRUTURA_RESERVAS

    antes = len(lista)
    nova_lista = [
        reserva for reserva in lista
        if not (reserva['hotel_id'] == hotelId and reserva['usuario_id'] == usuarioId)
    ]
    ESTRUTURA_RESERVAS = nova_lista

    if len(nova_lista) == antes:
        return 0  # Nenhuma reserva removida
    return 1  # Sucesso


# ======================
# Função: listar_reservas_por_usuario
# ======================
# Descrição:
# Lista todas as reservas feitas por um determinado usuário.
# Retorno:
# - Lista de reservas do usuário ou lista vazia.
def listar_reservas_por_usuario(usuario_id):
    global ESTRUTURA_RESERVAS
    dados = ESTRUTURA_RESERVAS
    return [r for r in dados if r["usuario_id"] == usuario_id]






