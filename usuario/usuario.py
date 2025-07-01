# =========================
# Diretivas de Entrada
# =========================
# - json: Biblioteca padrão usada para leitura e escrita de arquivos JSON.

import json

CAMINHO_ARQUIVO = "usuario/dadosUsuario.json"

# =========================
# Função: ler_todos_usuarios
# =========================
# Descrição:
# Lê a lista de usuários a partir do arquivo JSON no caminho CAMINHO_ARQUIVO.
# Se ocorrer um erro durante a leitura (como arquivo inexistente ou JSON malformado),
# retorna uma lista vazia.
# Acoplamento:
# - Depende do arquivo JSON localizado em CAMINHO_ARQUIVO.
# - Utiliza a biblioteca padrão json.
# Condições de Acoplamento:
# - O arquivo deve estar acessível e conter dados válidos no formato esperado.
# Hipóteses:
# - Cada item no JSON é um dicionário com as chaves: 'id', 'username' e 'senha'.
# Interface com o Usuário:
# - Emite mensagem de erro no console em caso de falha na leitura.

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
# Salva a lista de usuários no arquivo JSON em disco.
# Acoplamento:
# - Parâmetro:
#     - dados (list): Lista de dicionários contendo usuários.
# - Utiliza a biblioteca json.
# Condições de Acoplamento:
# - Entrada: Estrutura deve ser serializável em JSON.
# - Saída: Arquivo deve estar acessível para escrita.
# Interface com o Usuário:
# - Emite mensagem de erro no console em caso de falha.
# Retorno:
# - int: 0 para sucesso, 1 para erro ao salvar.

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
# Inicializa a estrutura de dados de usuários carregando os dados do arquivo JSON
# e armazenando na variável global ESTRUTURA_USUARIOS.
# Acoplamento:
# - Depende da função ler_todos_usuarios.
# Interface com o Usuário:
# - Exibe mensagem no console indicando a inicialização do módulo.

def iniciarModuloUsuario():
    global ESTRUTURA_USUARIOS
    ESTRUTURA_USUARIOS = ler_todos_usuarios()
    print('INICIADO USUARIO')


# =========================
# Função: obterUsuarios
# =========================
# Descrição:
# Retorna uma cópia da lista de usuários carregados em memória (ESTRUTURA_USUARIOS).
# Acoplamento:
# - Depende da variável global ESTRUTURA_USUARIOS.
# Interface com o Usuário:
# - Não interage diretamente com o usuário.

def obterUsuarios():
    global ESTRUTURA_USUARIOS
    return ESTRUTURA_USUARIOS[:]


# =========================
# Função: adicionarUsuario
# =========================
# Descrição:
# Adiciona um novo usuário à estrutura em memória, gerando um ID automaticamente.
# Acoplamento:
# - Parâmetros:
#     - username (str), senha (str)
# - Acessa e modifica ESTRUTURA_USUARIOS.
# Condições de Acoplamento:
# - username e senha devem ser válidos e não vazios.
# Hipóteses:
# - O controle de unicidade do username será feito externamente (não validado aqui).
# Interface com o Usuário:
# - Não interage com o usuário.
# Retorno:
# - dict: Dicionário do novo usuário criado.
# - None: Em caso de dados inválidos.

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
# Busca um usuário na estrutura em memória, com base no `criterio`.
# O critério pode ser o ID (int) ou o nome de usuário (str).
# Acoplamento:
# - Acessa ESTRUTURA_USUARIOS.
# Condições de Acoplamento:
# - A lista de usuários deve estar carregada e bem formada.
# Interface com o Usuário:
# - Não interage diretamente.
# Retorno:
# - list: Lista com um usuário correspondente (ou vazia se não houver).

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
# Valida se o par `username` e `senha` corresponde a algum usuário armazenado.
# Acoplamento:
# - Acessa ESTRUTURA_USUARIOS.
# Condições de Acoplamento:
# - A estrutura deve estar carregada corretamente.
# Interface com o Usuário:
# - Não interage diretamente.
# Retorno:
# - str:
#     - 'Senha correta'         : se as credenciais forem válidas.
#     - 'Senha incorreta'       : se o username existir mas a senha não coincidir.
#     - 'Usuário não cadastrado': se o username não for encontrado.

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









