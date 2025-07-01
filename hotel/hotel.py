import json
from reserva.reserva import obterReservas
import atexit


import json

CAMINHO_ARQUIVO = "hotel/dadosHotel.json"

# ======================
# Função: ler_todos_hoteis
# ======================
# Descrição:
# Lê todos os hotéis salvos no arquivo JSON. Retorna a lista de hotéis ou [] se ocorrer algum erro.
# Acoplamento:
# - Depende do arquivo JSON no caminho CAMINHO_ARQUIVO.
# Hipóteses:
# - O arquivo existe e contém uma lista válida de dicionários de hotéis.
# Interface com o Usuário:
# - Não há interação direta; falhas retornam listas vazias.

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
# Inicializa o módulo de hotéis carregando os dados do arquivo JSON.
# Acoplamento:
# - Depende de ler_todos_hoteis.
# Interface com o Usuário:
# - Exibe mensagem de sucesso na inicialização.

def iniciarModulo():
    global ESTRUTURA_HOTEIS
    ESTRUTURA_HOTEIS = ler_todos_hoteis()
    print('INICIADO HOTEL')


# ======================
# Função: salvar_todos
# ======================
# Descrição:
# Salva os dados fornecidos no arquivo JSON.
# Retorna:
# - 0: sucesso
# - 1: erro ao salvar
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
# Retorna todos os hotéis carregados em memória.
def obterHoteis():
    global ESTRUTURA_HOTEIS
    return ESTRUTURA_HOTEIS


# ======================
# Função: adicionarHotel
# ======================
# Descrição:
# Adiciona um novo hotel à estrutura e retorna o ID do novo hotel.
# Retornos:
# - ID do hotel criado
# - -1: Falha por dados incompletos
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
# Retorna hotéis cujo nome contém o critério fornecido (case-insensitive).
# Retornos:
# - Lista de hotéis encontrados.
# - Lista vazia se nenhum for encontrado ou critério inválido.
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
# Extrai os IDs dos hotéis a partir de uma lista de reservas.
# Hipóteses:
# - Cada reserva possui a chave 'hotel_id'.
def obterIdHoteisReservados(reservas):
    return [reserva['hotel_id'] for reserva in reservas if 'hotel_id' in reserva]


# ======================
# Função: obterHoteisPorIds
# ======================
# Descrição:
# Retorna os hotéis cujo ID está na lista fornecida.
# Retornos:
# - Lista de hotéis correspondentes.
def obterHoteisPorIds(ids: list):
    global ESTRUTURA_HOTEIS
    return [dado for dado in ESTRUTURA_HOTEIS if dado['id'] in ids]


# ======================
# Função: obterReservasComDadosCompletos
# ======================
# Descrição:
# Combina dados de reservas com os dados dos hotéis.
# Retorna lista contendo reservas com nome, descrição e datas.
# Retornos:
# - Lista de reservas enriquecidas com os dados dos hotéis.
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
# Filtra hotéis que ainda não foram reservados pelo usuário.
# Acoplamento:
# - Depende da função obterReservas().
# Hipóteses:
# - Cada reserva possui 'usuario_id' e 'hotel_id'.

def buscar_hoteis_disponiveis(usuario_id, hoteis):
    reservas = obterReservas()  # deve ser definida/importada no módulo de reservas

    hoteis_reservados_usuario = {reserva['hotel_id'] for reserva in reservas if reserva['usuario_id'] == usuario_id}
    hoteis_disponiveis = [hotel for hotel in hoteis if hotel['id'] not in hoteis_reservados_usuario]

    return hoteis_disponiveis
