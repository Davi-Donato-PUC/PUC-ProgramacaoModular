
import json
import os
from hotel.hotel import *

CAMINHO_ARQUIVO = "anfitriao/dadosAnfitriao.json"

# Função para ler todos os usuários
def ler_todos_anfitrioes():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []
    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

# Função para salvar todos os usuários
def salvar_anfitrioes(usuarios):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

# Função para adicionar um novo usuário
def adicionar_anfitriao(nome, senha):
    usuarios = ler_todos_anfitrioes()
    novo_id = 1 if not usuarios else max(u["id"] for u in usuarios) + 1

    novo_usuario = {
        "id": novo_id,
        "nome": nome,
        "senha": senha,
        "hoteis_id": []
    }
    usuarios.append(novo_usuario)
    salvar_anfitrioes(usuarios)
    print(f"Usuário '{nome}' adicionado com ID {novo_id}.")



def listarHoteisDoAnfitriao(hoteisIds) :
    hoteis = ler_todos_hoteis()
    hoteisAnf = []
    for hotel in hoteis : 
        if hotel['id'] in hoteisIds : 
            hoteisAnf.append(hotel)
    return hoteisAnf


def adicionarHotelAoAnfitriao(anfitriaoId, hotelId) :
    anfitrioes = ler_todos_anfitrioes()
    for anfitriao in anfitrioes :
        if anfitriao['id'] == anfitriaoId :
            print(type(anfitriao))
            anfitriao['hoteis_id'].append(hotelId)
    salvar_anfitrioes(anfitrioes)


def obterHoteisDoAnfitriao(id) :
    anfitrioes = ler_todos_anfitrioes()
    lh = []
    for a in anfitrioes :
        if id == a['id'] :
            lh = a['hoteis_id']
            return lh


