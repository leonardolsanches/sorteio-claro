from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime
import random

app = Flask(__name__)
DADOS_JSON = "dados.json"

def carregar_dados():
    if os.path.exists(DADOS_JSON):
        with open(DADOS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "livro1": [],
        "livro2": []
    }

def salvar_dados(dados):
    with open(DADOS_JSON, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    agora = datetime.now()
    sorteio_data = datetime(2025, 4, 18, 18, 0, 0)
    restante = (sorteio_data - agora).total_seconds()
    return render_template("index.html", tempo_restante=restante)

@app.route("/resumo/<livro>")
def resumo(livro):
    dados = carregar_dados()
    participantes = dados.get(livro, [])
    return render_template("resumo.html", participantes=participantes, livro=livro)

@app.route("/cadastro", methods=["POST"])
def cadastro():
    nome = request.form["nome"]
    email = request.form["email"].lower()
    livros = request.form.getlist("livros")

    if not email.endswith("@claro.com.br"):
        return "Apenas e-mails @claro.com.br podem se inscrever no sorteio."

    dados = carregar_dados()

    # Remove o usuário se já estiver cadastrado
    for lista in ["livro1", "livro2"]:
        dados[lista] = [p for p in dados[lista] if p["email"] != email]

    novo = {"nome": nome, "email": email}

    if "livro1" in livros:
        dados["livro1"].append(novo)
    if "livro2" in livros:
        dados["livro2"].append(novo)

    salvar_dados(dados)
    return redirect(url_for("index"))

@app.route("/sorteio_final")
def sorteio_final():
    dados = carregar_dados()

    participantes_livro1 = dados.get("livro1", [])
    participantes_livro2 = dados.get("livro2", [])

    ganhador1 = random.choice(participantes_livro1) if participantes_livro1 else None
    candidatos_livro2 = [p for p in participantes_livro2 if ganhador1 is None or p['email'] != ganhador1['email']]
    ganhador2 = random.choice(candidatos_livro2) if candidatos_livro2 else None

    return render_template("sorteio_final.html", livro1=ganhador1, livro2=ganhador2)

if __name__ == "__main__":
    app.run(debug=True)
