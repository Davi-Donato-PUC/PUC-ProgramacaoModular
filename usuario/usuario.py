
import json


CAMINHO_ARQUIVO = "usuario/dadosUsuario.json"


def ler_todos_usuarios():
    with open(CAMINHO_ARQUIVO, "r") as f:
        return json.load(f)


def salvar_todos(dados):
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(dados, f, indent=2)


def adicionarUsuario(username, senha):
    dados = ler_todos_usuarios()
    novo_id = 1 if not dados else max(item["id"] for item in dados) + 1
    novo = {"id": novo_id, "username": username, "senha": senha }
    dados.append(novo)
    salvar_todos(dados)
    return novo


def buscarUsuario(criterio):
    dados = ler_todos_usuarios()
    resultados = []

    if isinstance(criterio, int):
        resultados = [item for item in dados if item["id"] == criterio]
    elif isinstance(criterio, str):
        criterio_lower = criterio.lower()
        resultados = [item for item in dados if criterio_lower == item["username"].lower()]
    
    return resultados


def validarUsuario(username, senha) :
    users = ler_todos_usuarios()
    usuario = None

    for user in users :
        if user['username'] == username : 
            usuario = user
            break
    if usuario :
        if usuario['senha'] == senha :
            return 'Senha correta'
        else : 
            return 'Senha incorreta'
    else : return 'Usuário não cadastrado'




















