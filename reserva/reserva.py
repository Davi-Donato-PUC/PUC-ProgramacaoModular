# ======================
# Diretivas de Entrada
# ======================
# - json: Biblioteca padrão usada para leitura e escrita de arquivos JSON.

import json

CAMINHO_ARQUIVO = "reserva/dadosReserva.json"

# ======================
# Função: ler_todas_reservas
# ======================
# Descrição:
# Lê todas as reservas salvas no arquivo JSON definido por CAMINHO_ARQUIVO.
# Retorna uma lista de reservas se a leitura for bem-sucedida ou uma lista vazia em caso de erro.
# Acoplamento:
# - Depende da biblioteca json e do arquivo CAMINHO_ARQUIVO.
# Condições de Acoplamento:
# - O arquivo deve existir e conter uma lista de dicionários válidos.
# Hipóteses:
# - Cada item do JSON representa uma reserva com os campos esperados.
# Interface com o Usuário:
# - Imprime mensagem de erro no console se ocorrer falha na leitura.

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
# Salva a lista de reservas no arquivo JSON em disco.
# Acoplamento:
# - Parâmetro:
#     - dados (list): Lista de dicionários contendo reservas.
# - Utiliza a biblioteca json e o caminho CAMINHO_ARQUIVO.
# Condições de Acoplamento:
# - Entrada: Estrutura deve ser serializável em JSON.
# - Saída: Arquivo deve estar acessível para escrita.
# Interface com o Usuário:
# - Imprime mensagem de erro no console em caso de falha.
# Retornos:
# - int: 0 se sucesso, 1 se erro ao salvar.

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
# Inicializa o módulo de reservas carregando os dados do arquivo JSON em memória.
# Armazena os dados na variável global ESTRUTURA_RESERVAS.
# Acoplamento:
# - Depende da função ler_todas_reservas.
# Interface com o Usuário:
# - Imprime mensagem no console informando a inicialização do módulo.

def iniciarModuloReserva():
    global ESTRUTURA_RESERVAS
    ESTRUTURA_RESERVAS = ler_todas_reservas()
    print('INICIADO RESERVAS')


# ======================
# Função: obterReservas
# ======================
# Descrição:
# Retorna a estrutura de reservas atualmente carregada na memória.
# Acoplamento:
# - Depende da variável global ESTRUTURA_RESERVAS.
# Interface com o Usuário:
# - Não interage diretamente com o usuário.
# Retorno:
# - list: Cópia da lista de reservas.

def obterReservas():
    global ESTRUTURA_RESERVAS
    return ESTRUTURA_RESERVAS[:]


# ======================
# Função: adicionarReserva
# ======================
# Descrição:
# Adiciona uma nova reserva à estrutura em memória, caso ainda não exista uma reserva
# para o mesmo hotel. O ID da nova reserva é gerado automaticamente.
# Acoplamento:
# - Parâmetros:
#     - hotelId (int), usuarioId (int), checkin (str), checkout (str)
# - Acessa e modifica a variável global ESTRUTURA_RESERVAS.
# Condições de Acoplamento:
# - Todos os parâmetros devem estar preenchidos.
# - A estrutura em memória deve estar carregada corretamente.
# Hipóteses:
# - Apenas uma reserva por hotel é permitida.
# Interface com o Usuário:
# - Não interage diretamente.
# Retornos:
# - int: 
#     - -1: Dados incompletos
#     -  0: Reserva já existente para o hotel
#     - >0: ID da nova reserva criada

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
# Remove a reserva associada a um usuário e hotel específicos.
# Acoplamento:
# - Parâmetros:
#     - hotelId (int), usuarioId (int)
# - Modifica a variável global ESTRUTURA_RESERVAS.
# Condições de Acoplamento:
# - A reserva deve existir na estrutura.
# Interface com o Usuário:
# - Não interage com o usuário.
# Retornos:
# - int:
#     - 0: Nenhuma reserva foi encontrada para remoção.
#     - 1: Reserva removida com sucesso.

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
# Retorna uma lista contendo todas as reservas realizadas por um determinado usuário.
# Acoplamento:
# - Parâmetro:
#     - usuario_id (int)
# - Acessa a variável global ESTRUTURA_RESERVAS.
# Condições de Acoplamento:
# - A estrutura deve estar corretamente carregada e conter reservas válidas.
# Interface com o Usuário:
# - Não interage diretamente.
# Retorno:
# - list: Lista de reservas feitas pelo usuário.

def listar_reservas_por_usuario(usuario_id):
    global ESTRUTURA_RESERVAS
    dados = ESTRUTURA_RESERVAS
    return [r for r in dados if r["usuario_id"] == usuario_id]
