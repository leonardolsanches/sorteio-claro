from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Página inicial (carrega o dashboard)
@app.route('/')
def index():
    return render_template('dashboard.html')

# Retorna as alocações de um mês/ano
@app.route('/alocacoes')
def get_alocacoes():
    mes = request.args.get('mes')
    ano = request.args.get('ano')
    path = os.path.join('data', 'dados.json')
    with open(path) as f:
        data = json.load(f)
    return jsonify(data.get(f"{ano}-{mes}", {}))

# Recebe alocações novas
@app.route('/alocar', methods=['POST'])
def alocar():
    novo = request.json
    data_key = f"{novo['ano']}-{novo['mes']}"
    path = os.path.join('data', 'dados.json')
    with open(path, 'r+') as f:
        data = json.load(f)
        if data_key not in data:
            data[data_key] = {}
        for dia in novo['dias']:
            data[data_key][dia] = {
                "valor": novo['valor'],
                "atividade": novo['atividade'],
                "projeto": novo['projeto']
            }
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    return jsonify({"status": "ok"})

# Servir dados fixos como JSON (usuários, projetos, etc.)
@app.route('/data/<path:filename>')
def get_data_file(filename):
    return send_from_directory('data', filename)

# Servir arquivos estáticos (JS, CSS, imagens)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Inicialização local
if __name__ == '__main__':
    app.run(debug=True)
