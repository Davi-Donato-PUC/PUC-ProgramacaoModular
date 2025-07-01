# ======================
# Diretivas de Entrada
# ======================
# - json: Biblioteca padrão usada para leitura e escrita de arquivos JSON.
# - reserva.reserva.obterReservas: Função externa utilizada para obter as reservas dos hotéis.

import json
from reserva.reserva import obterReservas


CAMINHO_ARQUIVO = "hotel/dadosHotel.json"

# ======================
# Função: ler_todos_hoteis
# ======================
# Descrição:
# A função lê todos os hotéis salvos no arquivo JSON localizado em CAMINHO_ARQUIVO.
# Retorna a lista de hotéis se a leitura for bem-sucedida ou uma lista vazia em caso de erro.
# Acoplamento:
# - Depende do arquivo JSON em CAMINHO_ARQUIVO e da biblioteca json.
# Condições de Acoplamento:
# - O arquivo deve existir e conter uma lista de dicionários representando hotéis.
# Hipóteses:
# - O JSON está bem formatado.
# Interface com o Usuário:
# - Emite mensagens de erro no console, sem interação direta com o usuário.

def ler_todos_hoteis():
    try:
        with open(CAMINHO_ARQUIVO, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRO] Falha ao ler hotéis: {e}")
        return []


# ======================
# Função: iniciarModulo
# ======================
# Descrição:
# Inicializa o módulo de hotéis, carregando a estrutura ESTRUTURA_HOTEIS a partir do arquivo JSON.
# Acoplamento:
# - Depende da função ler_todos_hoteis.
# Hipóteses:
# - O arquivo de dados existe e está bem formatado.
# Interface com o Usuário:
# - Imprime no console uma mensagem indicando a inicialização bem-sucedida.

def iniciarModulo():
    global ESTRUTURA_HOTEIS
    ESTRUTURA_HOTEIS = ler_todos_hoteis()
    print('INICIADO HOTEL')


# ======================
# Função: salvar_todos
# ======================
# Descrição:
# Salva os dados fornecidos no arquivo JSON de hotéis.
# Acoplamento:
# - Parâmetros:
#     - dados (list): Lista de dicionários representando hotéis.
# - Retorno:
#     - int: 0 se sucesso, 1 se erro ao salvar.
# Condições de Acoplamento:
# - Entrada: Estrutura de dados válida.
# - Saída: Arquivo JSON atualizado corretamente.
# Interface com o Usuário:
# - Emite mensagem de erro no console em caso de falha.

def salvar_todos(dados):
    try:
        with open(CAMINHO_ARQUIVO, "w") as f:
            json.dump(dados, f, indent=2)
        return 0
    except Exception as e:
        print(f"[ERRO] Falha ao salvar hotéis: {e}")
        return 1


# ======================
# Função: obterHoteis
# ======================
# Descrição:
# Retorna todos os hotéis atualmente armazenados em memória (ESTRUTURA_HOTEIS).
# Acoplamento:
# - Depende da variável global ESTRUTURA_HOTEIS.
# Interface com o Usuário:
# - Não interage com o usuário.

def obterHoteis():
    global ESTRUTURA_HOTEIS
    return ESTRUTURA_HOTEIS[:]


# ======================
# Função: adicionarHotel
# ======================
# Descrição:
# Adiciona um novo hotel à estrutura de dados ESTRUTURA_HOTEIS.
# Gera um ID incremental automaticamente.
# Acoplamento:
# - Parâmetros:
#     - nome (str), preco (float/int), descricao (str)
# - Retorno:
#     - int: ID do novo hotel se sucesso, -1 se dados incompletos.
# Condições de Acoplamento:
# - Entrada: Todos os campos devem estar preenchidos.
# Interface com o Usuário:
# - Não interage com o usuário.

def adicionarHotel(nome, preco, descricao):
    global ESTRUTURA_HOTEIS

    if not nome or not preco or not descricao:
        return -1

    dados = ESTRUTURA_HOTEIS
    novo_id = 1 if not dados else max(item["id"] for item in dados) + 1
    novo = {"id": novo_id, "nome": nome, "preco": preco, "descricao": descricao}
    dados.append(novo)
    return novo_id


# ======================
# Função: buscarHoteis
# ======================
# Descrição:
# Busca hotéis cujo nome contenha a string `criterio` (case-insensitive).
# Acoplamento:
# - Parâmetro:
#     - criterio (str)
# - Retorno:
#     - list: Lista de hotéis correspondentes ou vazia.
# Condições de Acoplamento:
# - Entrada: criterio deve ser string.
# Interface com o Usuário:
# - Não interage com o usuário.

def buscarHoteis(criterio):
    global ESTRUTURA_HOTEIS

    if not isinstance(criterio, str):
        return []

    criterio_lower = criterio.lower()
    resultados = [item for item in ESTRUTURA_HOTEIS if criterio_lower in item["nome"].lower()]
    return resultados


# ======================
# Função: obterIdHoteisReservados
# ======================
# Descrição:
# A partir de uma lista de reservas, retorna uma lista com os IDs dos hotéis reservados.
# Acoplamento:
# - Parâmetro: lista de reservas (list)
# Condições de Acoplamento:
# - Cada reserva deve conter a chave 'hotel_id'.
# Interface com o Usuário:
# - Não interage com o usuário.

def obterIdHoteisReservados(reservas):
    return [reserva['hotel_id'] for reserva in reservas if 'hotel_id' in reserva]


# ======================
# Função: obterHoteisPorIds
# ======================
# Descrição:
# Retorna uma lista de hotéis cujos IDs estão na lista fornecida.
# Acoplamento:
# - Parâmetro: ids (list of int)
# - Usa a variável global ESTRUTURA_HOTEIS.
# Interface com o Usuário:
# - Não interage com o usuário.

def obterHoteisPorIds(ids: list):
    global ESTRUTURA_HOTEIS
    return [dado for dado in ESTRUTURA_HOTEIS if dado['id'] in ids]


# ======================
# Função: obterReservasComDadosCompletos
# ======================
# Descrição:
# Une os dados de reserva com as informações do hotel.
# Cada item da lista final contém nome, preço, descrição, checkin e checkout.
# Acoplamento:
# - Parâmetro: reservas (list)
# - Acessa ESTRUTURA_HOTEIS para dados dos hotéis.
# Interface com o Usuário:
# - Não interage com o usuário.

def obterReservasComDadosCompletos(reservas):
    global ESTRUTURA_HOTEIS
    resultado = []

    for reserva in reservas:
        hotel_id = reserva.get('hotel_id')
        hotel = next((h for h in ESTRUTURA_HOTEIS if h['id'] == hotel_id), None)
        if hotel:
            entrada = {
                'checkin': reserva.get('checkin'),
                'checkout': reserva.get('checkout'),
                **hotel
            }
            resultado.append(entrada)
    return resultado


# ======================
# Função: buscar_hoteis_disponiveis
# ======================
# Descrição:
# Retorna a lista de hotéis disponíveis para um determinado usuário, ou seja,
# hotéis que ele ainda não reservou.
# Acoplamento:
# - Depende da função externa obterReservas (importada de reserva.reserva).
# - Parâmetros:
#     - usuario_id (int): ID do usuário.
#     - hoteis (list): Lista de hotéis disponíveis.
# Condições de Acoplamento:
# - Cada reserva deve conter 'usuario_id' e 'hotel_id'.
# Interface com o Usuário:
# - Não interage com o usuário.

def buscar_hoteis_disponiveis(usuario_id, hoteis):
    reservas = obterReservas()

    hoteis_reservados_usuario = {reserva['hotel_id'] for reserva in reservas if reserva['usuario_id'] == usuario_id}
    hoteis_disponiveis = [hotel for hotel in hoteis if hotel['id'] not in hoteis_reservados_usuario]

    return hoteis_disponiveis
