from flask import Flask, render_template, request, redirect
import json
import os
import random
from datetime import datetime

app = Flask(__name__)

DADOS_PATH = "dados.json"

# Lista inicial para fallback se o JSON não existir ainda
dados_iniciais = [
    {"nome": "Washington Almeida", "email": "washington.almeida@claro.com.br", "livros": ["livro2"]},
    {"nome": "Cecilia Ramos", "email": "cecilia.ramos@claro.com.br", "livros": ["livro2"]},
    {"nome": "Marco Antonio Belarmino", "email": "marco.belarmino@claro.com.br", "livros": ["livro1", "livro2"]},
    {"nome": "Norberto Tomiyoshi Imamura", "email": "norberto.imamura@claro.com.br", "livros": ["livro1", "livro2"]},
    {"nome": "Kenia Pena de Souza", "email": "kenia.souza@claro.com.br", "livros": ["livro1"]},
    {"nome": "Sueli Teixeira da Silva", "email": "sueli.teixeira@claro.com.br", "livros": ["livro1", "livro2"]},
    {"nome": "Barbara Pizane", "email": "barbara.azevedodepaula@claro.com.br", "livros": ["livro1", "livro2"]},
    {"nome": "Maria Lucia Taborda Masiero", "email": "maria.masiero@claro.com.br", "livros": ["livro1", "livro2"]},
    {"nome": "Elisangela Iel", "email": "elisangela.iel@claro.com.br", "livros": ["livro1", "livro2"]}
]

def carregar_dados():
    if not os.path.exists(DADOS_PATH):
        with open(DADOS_PATH, "w") as f:
            json.dump(dados_iniciais, f, indent=4)
    with open(DADOS_PATH, "r") as f:
        return json.load(f)

def salvar_dados(lista):
    with open(DADOS_PATH, "w") as f:
        json.dump(lista, f, indent=4)

@app.route("/")
def index():
    dados = carregar_dados()
    return render_template("index.html", participantes=dados)

@app.route("/resumo_livro1")
def resumo_livro1():
    dados = carregar_dados()
    inscritos = [p for p in dados if "livro1" in p["livros"]]
    return render_template("resumo_livro1.html", participantes=inscritos)

@app.route("/resumo_livro2")
def resumo_livro2():
    dados = carregar_dados()
    inscritos = [p for p in dados if "livro2" in p["livros"]]
    return render_template("resumo_livro2.html", participantes=inscritos)

@app.route("/cadastro", methods=["POST"])
def cadastro():
    nome = request.form.get("nome")
    email = request.form.get("email")
    livros = request.form.getlist("livros")

    if not email.endswith("@claro.com.br"):
        return "Sorteio restrito aos e-mails @claro.com.br"

    dados = carregar_dados()

    # Evita duplicidade
    for p in dados:
        if p["email"] == email:
            return "Você já está inscrito."

    novo = {"nome": nome, "email": email, "livros": livros}
    dados.append(novo)
    salvar_dados(dados)

    return redirect("/")

@app.route("/sorteio_final")
def sorteio_final():
    dados = carregar_dados()
    participantes_livro1 = [p for p in dados if "livro1" in p["livros"]]
    participantes_livro2 = [p for p in dados if "livro2" in p["livros"]]

    ganhador1 = random.choice(participantes_livro1) if participantes_livro1 else None

    # Remove ganhador1 da lista do livro2 (pelo e-mail)
    candidatos_livro2 = [p for p in participantes_livro2 if ganhador1 is None or p["email"] != ganhador1["email"]]
    ganhador2 = random.choice(candidatos_livro2) if candidatos_livro2 else None

    return render_template("sorteio_final.html", livro1=ganhador1, livro2=ganhador2)

@app.route("/contador")
def contador():
    sorteio_datetime = datetime(2025, 4, 18, 18, 0, 0)
    agora = datetime.now()
    restante = sorteio_datetime - agora
    segundos_restantes = max(int(restante.total_seconds()), 0)
    return {"segundos": segundos_restantes}

if __name__ == "__main__":
    app.run(debug=True)
