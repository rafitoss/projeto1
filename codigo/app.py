import os
from flask import Flask, request, jsonify, render_template, session
from datetime import datetime
from queries import salvar_query, listar_queries, carregar_query, QUERIES_DIR
from processo import salvar_processo, listar_processos, carregar_processo, criar_processo_interativo

app = Flask(__name__)
app.secret_key = "chave-super-secreta"  # necessário para usar sessão

# Usuários válidos (simples)
USUARIOS = {
    "DBA": "123"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    user = data.get("usuario")
    senha = data.get("senha")

    if user in USUARIOS and USUARIOS[user] == senha:
        session["usuario"] = user
        return jsonify({"message": "Login bem-sucedido!", "usuario": user})
    else:
        return jsonify({"error": "Usuário ou senha incorretos."}), 401

@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop("usuario", None)
    return jsonify({"message": "Logout realizado com sucesso!"})

@app.route("/api/salvar", methods=["POST"])
def api_salvar():
    if "usuario" not in session:
        return jsonify({"error": "Não autenticado"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados inválidos ou ausentes."}), 400

    required = ["titulo", "query", "motivo", "ambiente", "autor"]
    for campo in required:
        if not data.get(campo):
            return jsonify({"error": f"Campo obrigatório: {campo}"}), 400

    data["data"] = datetime.today().strftime("%Y-%m-%d")

    try:
        salvar_query(data)
        return jsonify({"message": "Query salva com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/consultar")
def api_consultar():
    if "usuario" not in session:
        return jsonify({"error": "Não autenticado"}), 403

    arquivos = listar_queries()
    queries = []
    for arq in arquivos:
        data = carregar_query(arq)
        if data:
            queries.append(data)
    queries.sort(key=lambda x: x.get("data", "").upper())
    return jsonify(queries)


@app.route("/api/salvarp", methods=["POST"])
def api_salvarp():
    if "usuario" not in session:
        return jsonify({"error": "Não autenticado"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados inválidos ou ausentes."}), 400

    required = ["titulo", "servidor", "etapas", "autor"]
    for campo in required:
        if not data.get(campo):
            return jsonify({"error": f"Campo obrigatório: {campo}"}), 400

    data["data"] = datetime.today().strftime("%Y-%m-%d")

    try:
        salvar_processo(data)
        return jsonify({"message": "Processo salvo com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/consultarp")
def api_consultarp():
    if "usuario" not in session:
        return jsonify({"error": "Não autenticado"}), 403

    arquivos = listar_processos()
    processo = []
    for arq in arquivos:
        data = carregar_processo(arq)
        if data:
            processo.append(data)
    processo.sort(key=lambda x: x.get("data", "").upper())
    return jsonify(processo)


@app.route("/api/apagar_query/<arquivo>", methods=["DELETE"])
def api_apagar_query(arquivo):
    if "usuario" not in session:
        return jsonify({"error": "Não autenticado"}), 403

    path = os.path.join(QUERIES_DIR, arquivo)
    if not os.path.exists(path):
        return jsonify({"error": "Arquivo não encontrado"}), 404

    try:
        os.remove(path)
        return jsonify({"message": f"Arquivo '{arquivo}' apagado com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":
    app.run(debug=True)



@app.route("/api/abrir_query/<arquivo>")
def api_abrir_query(arquivo):
    if "usuario" not in session:
        return jsonify({"error": "Não autenticado"}), 403

    from queries import carregar_query

    data = carregar_query(arquivo)
    if not data:
        return jsonify({"error": "Arquivo não encontrado"}), 404

    return jsonify(data)



