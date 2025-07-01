
import json
import os
from hotel.hotel import obterHoteis
import atexit

import json
import os

CAMINHO_ARQUIVO = "anfitriao/dadosAnfitriao.json"

# =========================
# Função: ler_todos_anfitrioes
# =========================
# Descrição:
# Lê todos os anfitriões a partir do arquivo JSON. Se o arquivo não existir, retorna lista vazia.
# Acoplamento:
# - Depende do arquivo JSON estar no caminho correto e com estrutura válida.
# Hipóteses:
# - O JSON contém uma lista de dicionários com os campos 'id', 'nome', 'senha', 'hoteis_id'.
# Interface com o Usuário:
# - Sem interação direta.

def ler_todos_anfitrioes():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    try:
        with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except Exception as e:
        print(f"[ERRO] Falha ao ler anfitriões: {e}")
        return []


# =========================
# Função: salvar_anfitrioes
# =========================
# Descrição:
# Salva a lista de anfitriões no arquivo JSON.
# Retornos:
# - 0: sucesso
# - 1: erro ao salvar
def salvar_anfitrioes(usuarios):
    try:
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
        return 0
    except Exception as e:
        print(f"[ERRO] Falha ao salvar anfitriões: {e}")
        return 1


# =========================
# Função: iniciarModuloAnfitriao
# =========================
# Descrição:
# Inicializa o módulo carregando os dados dos anfitriões em memória.
def iniciarModuloAnfitriao():
    global ESTRUTURA_ANFITRIOES
    ESTRUTURA_ANFITRIOES = ler_todos_anfitrioes()
    print('INICIADO ANFITRIAO')


# =========================
# Função: obterAnfitrioes
# =========================
# Descrição:
# Retorna todos os anfitriões carregados na memória.
def obterAnfitrioes():
    global ESTRUTURA_ANFITRIOES
    return ESTRUTURA_ANFITRIOES


# =========================
# Função: adicionar_anfitriao
# =========================
# Descrição:
# Adiciona um novo anfitrião ao sistema.
# Hipóteses:
# - Nome de usuário e senha são válidos e únicos.
# Retornos:
# - Dicionário do novo anfitrião.
# - None: se dados inválidos.
def adicionar_anfitriao(nome, senha):
    global ESTRUTURA_ANFITRIOES

    if not nome or not senha:
        return None  # dados incompletos

    usuarios = ESTRUTURA_ANFITRIOES
    novo_id = 1 if not usuarios else max(u["id"] for u in usuarios) + 1

    novo_usuario = {
        "id": novo_id,
        "nome": nome,
        "senha": senha,
        "hoteis_id": []
    }
    usuarios.append(novo_usuario)
    return novo_usuario


# =========================
# Função: listarHoteisDoAnfitriao
# =========================
# Descrição:
# Recebe uma lista de IDs de hotéis e retorna os dados completos desses hotéis.
# Acoplamento:
# - Depende da função obterHoteis() do módulo de hotéis.
def listarHoteisDoAnfitriao(hoteisIds):
    hoteis = obterHoteis()  # esta função deve estar disponível/importada do módulo de hotéis
    hoteisAnf = [hotel for hotel in hoteis if hotel['id'] in hoteisIds]
    return hoteisAnf


# =========================
# Função: adicionarHotelAoAnfitriao
# =========================
# Descrição:
# Adiciona um hotel à lista de hotéis gerenciados por um anfitrião específico.
# Hipóteses:
# - ID do anfitrião existe.
# Retornos:
# - 0: anfitrião não encontrado
# - 1: hotel adicionado com sucesso
def adicionarHotelAoAnfitriao(anfitriaoId, hotelId):
    global ESTRUTURA_ANFITRIOES
    anfitrioes = ESTRUTURA_ANFITRIOES

    for anfitriao in anfitrioes:
        if anfitriao['id'] == anfitriaoId:
            if hotelId not in anfitriao['hoteis_id']:
                anfitriao['hoteis_id'].append(hotelId)
            return 1
    return 0


# =========================
# Função: obterHoteisDoAnfitriao
# =========================
# Descrição:
# Retorna a lista de IDs de hotéis que um anfitrião administra.
# Retornos:
# - Lista de IDs de hotéis.
# - []: se anfitrião não for encontrado.
def obterHoteisDoAnfitriao(id):
    global ESTRUTURA_ANFITRIOES
    anfitrioes = ESTRUTURA_ANFITRIOES

    for anfitriao in anfitrioes:
        if anfitriao['id'] == id:
            return anfitriao['hoteis_id']
    return []
