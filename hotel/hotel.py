import json

CAMINHO_ARQUIVO = "hotel/dadosHotel.json"

def ler_todos():
    with open(CAMINHO_ARQUIVO, "r") as f:
        return json.load(f)

def salvar_todos(dados):
    with open(CAMINHO_ARQUIVO, "w") as f:
        json.dump(dados, f, indent=2)

def adicionarHotel(nome, preco, descricao):
    dados = ler_todos()
    novo_id = 1 if not dados else max(item["id"] for item in dados) + 1
    novo = {"id": novo_id, "nome": nome, "preco": preco, "descricao": descricao}
    dados.append(novo)
    salvar_todos(dados)
    print(f"Elemento adicionado: {novo}")

def buscarHotel(criterio):
    dados = ler_todos()
    resultados = []

    if isinstance(criterio, int):
        # Busca por ID exato
        resultados = [item for item in dados if item["id"] == criterio]
    elif isinstance(criterio, str):
        # Busca por parte do nome (ignora maiúsculas/minúsculas)
        criterio_lower = criterio.lower()
        resultados = [item for item in dados if criterio_lower in item["nome"].lower()]
    
    return resultados



