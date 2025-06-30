import json
from reserva.reserva import ler_todas_reservas
CAMINHO_ARQUIVO = "hotel/dadosHotel.json"

def ler_todos_hoteis():
    with open(CAMINHO_ARQUIVO, "r") as f:
        return json.load(f)

def salvar_todos(dados):
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(dados, f, indent=2)

def adicionarHotel(nome, preco, descricao):
    dados = ler_todos_hoteis()
    novo_id = 1 if not dados else max(item["id"] for item in dados) + 1
    novo = {"id": novo_id, "nome": nome, "preco": preco, "descricao": descricao}
    dados.append(novo)
    salvar_todos(dados)
    return novo_id
  

def buscarHoteis(criterio):
    dados = ler_todos_hoteis()
    resultados = []


    if isinstance(criterio, str):
        # Busca por parte do nome (ignora maiúsculas/minúsculas)
        criterio_lower = criterio.lower()
        resultados = [item for item in dados if criterio_lower in item["nome"].lower()]
    
    return resultados


def obterHoteisPorIds(ids:list) :
    dados = ler_todos_hoteis()
    hoteis = []
    for dado in dados :
        if dado['id'] in ids : hoteis.append(dado)
    return hoteis



def buscar_hoteis_disponiveis(usuario_id, hoteis):
    reservas = ler_todas_reservas()

    # Coletar os IDs dos hotéis que já estão reservados por esse usuário
    hoteis_reservados_usuario = {reserva['hotel_id'] for reserva in reservas if reserva['usuario_id'] == usuario_id}

    # Filtrar hotéis que não estão reservados por esse usuário
    hoteis_disponiveis = [hotel for hotel in hoteis if hotel['id'] not in hoteis_reservados_usuario]

    return hoteis_disponiveis
