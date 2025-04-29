from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random
from datetime import datetime

app = Flask(__name__)

DADOS_PATH = "dados.json"
GANHADORES_PATH = "ganhadores.json"
SORTEIO_DATA_HORA = datetime(2025, 7, 31, 18, 0, 0)

def carregar_dados():
    if os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_dados(lista):
    with open(DADOS_PATH, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4)

def carregar_ganhadores():
    if os.path.exists(GANHADORES_PATH):
        with open(GANHADORES_PATH, "r") as f:
            return json.load(f)
    return None

def salvar_ganhadores(g1, g2):
    with open(GANHADORES_PATH, "w") as f:
        json.dump({ "livro1": g1, "livro2": g2 }, f, indent=4)

@app.route("/")
def index():
    dados = carregar_dados()
    return render_template("index.html", participantes=dados)

@app.route("/cadastro", methods=["POST"])
def cadastro():
    if datetime.now() >= SORTEIO_DATA_HORA:
        return "O sorteio foi encerrado. As inscrições não estão mais disponíveis."

    nome = request.form.get("nome")
    email = request.form.get("email").lower()
    livro = request.form.get("livros")

    if not email.endswith("@claro.com.br"):
        return "Cadastro não autorizado. Domínio do e-mail inválido."

    dados = carregar_dados()
    for p in dados:
        if p["email"] == email:
            return "Este e-mail já está inscrito."

    livros = []
    if livro == "livro1":
        livros = ["livro1"]
    elif livro == "livro2":
        livros = ["livro2"]
    elif livro == "ambos":
        livros = ["livro1", "livro2"]

    novo = { "nome": nome, "email": email, "livros": livros }
    dados.append(novo)
    salvar_dados(dados)

    return redirect(url_for("index"))

@app.route("/sorteio_final")
def sorteio_final():
    ganhadores = carregar_ganhadores()
    if ganhadores:
        return render_template("sorteio_final.html", livro1=ganhadores["livro1"], livro2=ganhadores["livro2"])

    if datetime.now() < SORTEIO_DATA_HORA:
        return "O sorteio ainda não ocorreu."

    dados = carregar_dados()
    participantes_livro1 = [p for p in dados if "livro1" in p["livros"]]
    participantes_livro2 = [p for p in dados if "livro2" in p["livros"]]

    ganhador1 = random.choice(participantes_livro1) if participantes_livro1 else None
    candidatos_livro2 = [p for p in participantes_livro2 if ganhador1 is None or p["email"] != ganhador1["email"]]
    ganhador2 = random.choice(candidatos_livro2) if candidatos_livro2 else None

    salvar_ganhadores(ganhador1, ganhador2)
    return render_template("sorteio_final.html", livro1=ganhador1, livro2=ganhador2)

@app.route("/livro1")
def livro1():
    return render_template("livro1.html")

@app.route("/livro2")
def livro2():
    return render_template("livro2.html")

if __name__ == "__main__":
    app.run(debug=True)
