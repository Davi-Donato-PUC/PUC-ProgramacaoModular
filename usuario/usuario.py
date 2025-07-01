
import json
import atexit


import json

CAMINHO_ARQUIVO = "usuario/dadosUsuario.json"

# =========================
# Função: ler_todos_usuarios
# =========================
# Descrição:
# Lê a lista de usuários a partir do arquivo JSON definido.
# Acoplamento:
# - Depende da existência de um arquivo JSON válido.
# Hipóteses:
# - O arquivo existe e contém uma lista de dicionários com chaves: 'id', 'username', 'senha'.
# Retorno:
# - Lista de usuários, ou [] em caso de erro de leitura.

def ler_todos_usuarios():
    try:
        with open(CAMINHO_ARQUIVO, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERRO] Falha ao ler usuários: {e}")
        return []


# =========================
# Função: salvar_todos
# =========================
# Descrição:
# Salva a lista de usuários no arquivo JSON.
# Retorno:
# - 0: sucesso
# - 1: erro ao salvar
def salvar_todos(dados):
    try:
        with open(CAMINHO_ARQUIVO, "w") as f:
            json.dump(dados, f, indent=2)
        return 0
    except Exception as e:
        print(f"[ERRO] Falha ao salvar usuários: {e}")
        return 1


# =========================
# Função: iniciarModuloUsuario
# =========================
# Descrição:
# Inicializa o módulo de usuários carregando os dados em memória.
# Interface com o Usuário:
# - Imprime mensagem de inicialização.
def iniciarModuloUsuario():
    global ESTRUTURA_USUARIOS
    ESTRUTURA_USUARIOS = ler_todos_usuarios()
    print('INICIADO USUARIO')


# =========================
# Função: obterUsuarios
# =========================
# Descrição:
# Retorna a estrutura de usuários carregada na memória.
def obterUsuarios():
    global ESTRUTURA_USUARIOS
    return ESTRUTURA_USUARIOS


# =========================
# Função: adicionarUsuario
# =========================
# Descrição:
# Adiciona um novo usuário à estrutura em memória.
# Hipóteses:
# - `username` não pode estar duplicado (não verificado aqui).
# Retorno:
# - Dicionário com os dados do novo usuário.
# - None: se dados forem inválidos.
def adicionarUsuario(username, senha):
    global ESTRUTURA_USUARIOS

    if not username or not senha:
        return None  # Dados incompletos

    dados = ESTRUTURA_USUARIOS
    novo_id = 1 if not dados else max(item["id"] for item in dados) + 1
    novo = {"id": novo_id, "username": username, "senha": senha}
    dados.append(novo)
    return novo


# =========================
# Função: buscarUsuario
# =========================
# Descrição:
# Busca usuários por ID (int) ou por username (str).
# Retorno:
# - Lista com os usuários encontrados (máximo 1 item).
# - Lista vazia: se nenhum encontrado.
def buscarUsuario(criterio):
    global ESTRUTURA_USUARIOS
    dados = ESTRUTURA_USUARIOS

    if isinstance(criterio, int):
        return [user for user in dados if user["id"] == criterio]
    elif isinstance(criterio, str):
        criterio_lower = criterio.lower()
        return [user for user in dados if criterio_lower == user["username"].lower()]
    
    return []  # Critério inválido


# =========================
# Função: validarUsuario
# =========================
# Descrição:
# Valida um par de `username` e `senha` com os dados existentes.
# Retornos:
# - 'Senha correta'      : credenciais válidas
# - 'Senha incorreta'    : username existe mas senha não bate
# - 'Usuário não cadastrado' : username não encontrado
def validarUsuario(username, senha):
    global ESTRUTURA_USUARIOS
    users = ESTRUTURA_USUARIOS

    for user in users:
        if user['username'] == username:
            if user['senha'] == senha:
                return 'Senha correta'
            else:
                return 'Senha incorreta'
    return 'Usuário não cadastrado'













