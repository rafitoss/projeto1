import os
import yaml
from datetime import datetime

QUERIES_DIR = "queries"

def salvar_query(data):
    if not os.path.exists(QUERIES_DIR):
        os.makedirs(QUERIES_DIR)

    titulo_formatado = data["titulo"].replace(" ", "_").lower()
    filename = f"{titulo_formatado}.yaml"
    path = os.path.join(QUERIES_DIR, filename)

    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)
    print(f"Query salva em: {path}")

def listar_queries():
    if not os.path.exists(QUERIES_DIR):
        return []

    arquivos = [f for f in os.listdir(QUERIES_DIR) if f.endswith(".yaml")]
    return arquivos

def carregar_query(nome_arquivo):

    path = os.path.join(QUERIES_DIR, nome_arquivo)
    if not os.path.exists(path):
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None

    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data

def criar_query_interativa():
    data = {
        "titulo": input("Título da query: "),
        "query": input("SQL: "),
        "motivo": input("Motivo: "),
        "ambiente": input("Ambiente (producao, homologacao, etc): "),
        "rollback": input("Rollback (se houver): "),
        "data": datetime.today().strftime("%Y-%m-%d-%hh-%mm-%ss"),
        "autor": input("Autor: ")
    }
    salvar_query(data)

# Execução via terminal
if __name__ == "__main__":
    print("1. Criar nova query")
    print("2. Listar queries")
    print("3. Ver uma query")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        criar_query_interativa()
    elif opcao == "2":
        queries = listar_queries()
        if queries:
            for q in queries:
                print(f"- {q}")
        else:
            print("Nenhuma query encontrada.")
    elif opcao == "3":
        nome = input("Nome do arquivo .yaml: ")
        data = carregar_query(nome)
        if data:
            print("\n--- Detalhes da Query ---")
            for k, v in data.items():
                print(f"{k.capitalize()}: {v}")
    else:
        print("Opção inválida.")
