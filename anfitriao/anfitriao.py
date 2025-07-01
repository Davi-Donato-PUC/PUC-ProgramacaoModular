# =========================
# Diretivas de Entrada
# =========================
# - json: Para leitura e escrita de arquivos JSON.
# - os: Para verificar existência de arquivos.
# - obterHoteis: Função importada do módulo hotel, usada para listar hotéis de um anfitrião.

import json
import os
from hotel.hotel import obterHoteis

CAMINHO_ARQUIVO = "anfitriao/dadosAnfitriao.json"

# =========================
# Função: ler_todos_anfitrioes
# =========================
# Descrição:
# Lê todos os anfitriões do arquivo JSON definido em CAMINHO_ARQUIVO.
# Retorna lista de dicionários ou [] se o arquivo não existir ou ocorrer erro.
# Acoplamento:
# - Depende do arquivo JSON existir e conter estrutura válida.
# - Usa a biblioteca json e os.path.
# Condições de Acoplamento:
# - O arquivo precisa estar acessível e com conteúdo JSON bem formatado.
# Hipóteses:
# - Cada anfitrião é um dicionário com as chaves 'id', 'nome', 'senha' e 'hoteis_id'.
# Interface com o Usuário:
# - Imprime erro no console, se houver falha.

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
# Acoplamento:
# - Usa json e CAMINHO_ARQUIVO.
# Condições de Acoplamento:
# - A lista de anfitriões deve ser serializável em JSON.
# - O arquivo deve ser acessível para escrita.
# Interface com o Usuário:
# - Emite erro no console, se necessário.
# Retornos:
# - int: 0 para sucesso, 1 em caso de erro.

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
# Inicializa a estrutura de anfitriões em memória a partir do arquivo JSON.
# Acoplamento:
# - Depende de ler_todos_anfitrioes.
# Interface com o Usuário:
# - Imprime mensagem indicando inicialização do módulo.

def iniciarModuloAnfitriao():
    global ESTRUTURA_ANFITRIOES
    ESTRUTURA_ANFITRIOES = ler_todos_anfitrioes()
    print('INICIADO ANFITRIAO')


# =========================
# Função: obterAnfitrioes
# =========================
# Descrição:
# Retorna uma cópia da lista de anfitriões atualmente carregada na memória.
# Acoplamento:
# - Depende da variável global ESTRUTURA_ANFITRIOES.
# Interface com o Usuário:
# - Não interage diretamente.
# Retorno:
# - list: Cópia da estrutura de anfitriões.

def obterAnfitrioes():
    global ESTRUTURA_ANFITRIOES
    return ESTRUTURA_ANFITRIOES[:]


# =========================
# Função: adicionar_anfitriao
# =========================
# Descrição:
# Adiciona um novo anfitrião com nome, senha e lista de hotéis vazia.
# Acoplamento:
# - Usa e modifica a estrutura global ESTRUTURA_ANFITRIOES.
# Condições de Acoplamento:
# - nome e senha devem ser válidos.
# Hipóteses:
# - O nome é único (não verificado aqui).
# Interface com o Usuário:
# - Não interage diretamente.
# Retornos:
# - dict: Dicionário do novo anfitrião.
# - None: Em caso de dados inválidos.

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
# Dado uma lista de IDs de hotéis, retorna os dados completos dos hotéis que o anfitrião possui.
# Acoplamento:
# - Depende da função obterHoteis() do módulo de hotéis.
# Interface com o Usuário:
# - Não interage diretamente.
# Retorno:
# - list: Lista de dicionários com dados dos hotéis.

def listarHoteisDoAnfitriao(hoteisIds):
    hoteis = obterHoteis()  # esta função deve estar disponível/importada do módulo de hotéis
    hoteisAnf = [hotel for hotel in hoteis if hotel['id'] in hoteisIds]
    return hoteisAnf


# =========================
# Função: adicionarHotelAoAnfitriao
# =========================
# Descrição:
# Adiciona o ID de um hotel à lista de hotéis de um anfitrião.
# Acoplamento:
# - Modifica ESTRUTURA_ANFITRIOES.
# Condições de Acoplamento:
# - O anfitrião deve existir e não deve já possuir o hotel.
# Hipóteses:
# - O ID do hotel é válido e já foi criado anteriormente.
# Interface com o Usuário:
# - Não interage diretamente.
# Retornos:
# - int:
#     - 0: anfitrião não encontrado
#     - 1: hotel adicionado com sucesso (ou já existente)

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
# Retorna a lista de IDs dos hotéis administrados por um anfitrião.
# Acoplamento:
# - Acessa ESTRUTURA_ANFITRIOES.
# Condições de Acoplamento:
# - O anfitrião deve existir na estrutura.
# Interface com o Usuário:
# - Não interage diretamente.
# Retornos:
# - list: Lista com IDs de hotéis, ou lista vazia se o anfitrião não for encontrado.

def obterHoteisDoAnfitriao(id):
    global ESTRUTURA_ANFITRIOES
    anfitrioes = ESTRUTURA_ANFITRIOES

    for anfitriao in anfitrioes:
        if anfitriao['id'] == id:
            return anfitriao['hoteis_id']
    return []
