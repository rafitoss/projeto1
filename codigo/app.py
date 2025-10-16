from flask import Flask, request, jsonify, render_template
from datetime import datetime
from queries import salvar_query, listar_queries, carregar_query

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/salvar", methods=["POST"])
def api_salvar():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Dados inválidos ou ausentes."}), 400

    required = ["titulo", "query", "motivo", "ambiente", "autor"]
    for campo in required:
        if not data.get(campo):
            return jsonify({"error": f"Campo obrigatório: {campo}"}), 400

    data["data"] = datetime.today().strftime("%Y-%m-%d")

    try:
        salvar_query(data)  # usa queries.py para salvar em YAML
        return jsonify({"message": "Query salva com sucesso!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/consultar')
def api_consultar():
    arquivos = listar_queries()
    queries = []
    for arq in arquivos:
        data = carregar_query(arq)
        if data:
            queries.append(data)
    # Ordenar pelo título ascendente
    queries.sort(key=lambda x: x.get("data", "").upper())
    return jsonify(queries)


if __name__ == "__main__":
    app.run(debug=True)
