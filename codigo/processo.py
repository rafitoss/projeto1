import os
import yaml
from datetime import datetime

PROCESSOS_DIR = "processos"  

def salvar_processo(data):
    if not os.path.exists(PROCESSOS_DIR):
        os.makedirs(PROCESSOS_DIR)

    titulo_formatado = data["titulo"].replace(" ", "_").lower()
    filename = f"{titulo_formatado}.yaml"
    path = os.path.join(PROCESSOS_DIR, filename)

    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)
    print(f"Processo salvo em: {path}")

def listar_processos():
    
    if not os.path.exists(PROCESSOS_DIR):
        return []
    return [f for f in os.listdir(PROCESSOS_DIR) if f.endswith(".yaml")]

def carregar_processo(nome_arquivo):
    
    path = os.path.join(PROCESSOS_DIR, nome_arquivo)
    if not os.path.exists(path):
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None

    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data

def criar_processo_interativo():
    
    titulo = input("Título do processo: ").strip()
    servidor = input("Servidor: ").strip()

    etapas = []
    while True:
        etapa = input("Adicionar etapa (ou ENTER para finalizar): ").strip()
        if not etapa:
            break
        etapas.append(etapa)

    rollback = input("Rollback (se houver): ").strip()
    autor = input("Autor: ").strip()
    ambiente = input("Ambiente (produção, homologação, etc): ").strip()
    data_criacao = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    processo = {
        "titulo": titulo,
        "servidor": servidor,
        "etapas": etapas,
        "rollback": rollback,
        "autor": autor,
        "ambiente": ambiente,
        "data": data_criacao
    }

    salvar_processo(processo)

# Execução via terminal
if __name__ == "__main__":
    print("1. Criar novo processo")
    print("2. Listar processos")
    print("3. Ver um processo")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        criar_processo_interativo()
    elif opcao == "2":
        processos = listar_processos()
        if processos:
            for p in processos:
                print(f"- {p}")
        else:
            print("Nenhum processo encontrado.")
    elif opcao == "3":
        nome = input("Nome do arquivo .yaml: ").strip()
        data = carregar_processo(nome)
        if data:
            print("\n--- Detalhes do Processo ---")
            for k, v in data.items():
                print(f"{k.capitalize()}: {v}")
    else:
        print("Opção inválida.")
