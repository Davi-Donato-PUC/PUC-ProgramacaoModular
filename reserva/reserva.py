import json

CAMINHO_ARQUIVO = "reserva/dadosReserva.json"


def ler_todas_reservas():
    with open(CAMINHO_ARQUIVO, "r") as f:
        return json.load(f)


def salvar_todos(dados):
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(dados, f, indent=2)


def adicionarReserva(hotelId, usuarioId) :
    dados = ler_todas_reservas()
    novo_id = 1 if not dados else max(item["id"] for item in dados) + 1

    # verificando se a reserva ja ta feita
    for dado in dados :
        if hotelId == dado['hotel_id'] : return 0

    novo = {"id": novo_id, "hotel_id": hotelId, "usuario_id": usuarioId }
    dados.append(novo)
    salvar_todos(dados)


def excluirReserva(hotelId, usuarioId) :
    lista = ler_todas_reservas()
    nova_lista = [reserva for reserva in lista if not (reserva['hotel_id'] == hotelId and reserva['usuario_id'] == usuarioId ) ]
    salvar_todos(nova_lista)



def listar_reservas_por_usuario(usuario_id):
    dados = ler_todas_reservas()
    return [b for b in dados if b["usuario_id"] == usuario_id]



def obterIdHoteisReservados(reservas) :
    ids = []
    for reserva in reservas :
        ids.append(reserva['hotel_id'])    
    return ids
    








