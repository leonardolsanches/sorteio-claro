from flask import Flask, render_template, request, redirect, url_for
import random
import json
import os

app = Flask(__name__)

# Inicializar listas
participantes_livro1 = []
participantes_livro2 = []
todos_participantes = []

DADOS_PATH = "dados.json"

# Carrega dados salvos (se existir)
if os.path.exists(DADOS_PATH):
    with open(DADOS_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)
        participantes_livro1 = dados.get("livro1", [])
        participantes_livro2 = dados.get("livro2", [])
        todos_participantes = dados.get("todos", [])

def salvar_dados():
    with open(DADOS_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "livro1": participantes_livro1,
            "livro2": participantes_livro2,
            "todos": todos_participantes
        }, f, indent=2, ensure_ascii=False)

@app.route('/')
def home():
    return render_template(
        'index.html',
        participantes=todos_participantes
    )

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form['nome']
    email = request.form['email'].lower()
    livro = request.form['livro']

    if not email.endswith('@claro.com.br'):
        return "Cadastro inválido. O sorteio é exclusivo para colaboradores da Claro."

    entrada = {'nome': nome, 'email': email, 'livro': livro}

    # Adiciona às listas específicas
    if livro == 'livro1' and email not in [p['email'] for p in participantes_livro1]:
        participantes_livro1.append(entrada)
    elif livro == 'livro2' and email not in [p['email'] for p in participantes_livro2]:
        participantes_livro2.append(entrada)
    elif livro == 'ambos':
        if email not in [p['email'] for p in participantes_livro1]:
            participantes_livro1.append({'nome': nome, 'email': email, 'livro': 'ambos'})
        if email not in [p['email'] for p in participantes_livro2]:
            participantes_livro2.append({'nome': nome, 'email': email, 'livro': 'ambos'})

    if email not in [p['email'] for p in todos_participantes]:
        todos_participantes.append(entrada)

    salvar_dados()
    return redirect(url_for('home'))

@app.route('/livro1')
def livro1():
    return render_template('livro1.html')

@app.route('/livro2')
def livro2():
    return render_template('livro2.html')

@app.route('/sorteio_livro1')
def sorteio_livro1():
    if participantes_livro1:
        sorteado = random.choice(participantes_livro1)
        return render_template('sorteio_livro1.html', pessoa=sorteado)
    return "Nenhum participante válido para o Livro 1."

@app.route('/sorteio_livro2')
def sorteio_livro2():
    if participantes_livro2:
        sorteado = random.choice(participantes_livro2)
        return render_template('sorteio_livro2.html', pessoa=sorteado)
    return "Nenhum participante válido para o Livro 2."

@app.route('/sorteio_final')
def sorteio_final():
    ganhador1 = None
    ganhador2 = None

    if not participantes_livro1 and not participantes_livro2:
        return "Nenhum participante cadastrado para nenhum dos livros."

    if participantes_livro1:
        ganhador1 = random.choice(participantes_livro1)

    candidatos_livro2 = [
        p for p in participantes_livro2 if ganhador1 is None or p['email'] != ganhador1['email']
    ]

    if candidatos_livro2:
        ganhador2 = random.choice(candidatos_livro2)

    return render_template(
        'sorteio_final.html',
        livro1=ganhador1,
        livro2=ganhador2
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
