import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request, flash
from flask_wtf.csrf import CSRFProtect

from db import execute_one, execute_query, execute_insert

from mysql.connector import Error

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Liga a proteção CSRF: todo formulário POST do sistema vai precisar do token
CSRFProtect(app)

# Anúncios de venda do dashboard (dados fictícios). Para mudar um anúncio, edite os valores.
# "imagem": cole entre aspas o endereço (link) da foto na internet.
# Se deixar vazio (""), o anúncio mostra um quadro cinza com um ícone de carro.
ANUNCIOS = [
    {
        "modelo": "Lancer GT 2.0",
        "marca": "Mitsubishi",
        "ano": 2014,
        "km": "135.000",
        "preco": "R$ 52.000,00",
        "imagem": "https://s3.ecompletocarros.dev/images/lojas/277/veiculos/35096/veiculoInfoVeiculoImagesMobile/vehicle_image_1599249815_f3ccdd27d2000e3f9255a7e3e2c48800.jpeg",
    },
    {
        "modelo": "Opala Comodoro 4.1",
        "marca": "Chevrolet",
        "ano": 1975,
        "km": "202.500",
        "preco": "R$ 79.900,00",
        "imagem": "https://www.webmotors.com.br/tabela-fipe/_next/image?url=https%3A%2F%2Fimage.webmotors.com.br%2F_fotos%2FAnuncioUsados%2Fgigante%2F2026%2F202609%2F20260919%2Fchevroletopala25deluxo8vgasolina2pmanual-WMIMAGEM21014013861.jpg&w=768&q=75",
    },
]

# ==============================================================================
# PÁGINAS PRINCIPAIS
# ==============================================================================

@app.route("/", methods=["GET", "POST"])
def inicio():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", anuncios=ANUNCIOS)

# ==============================================================================
# USUÁRIOS
# ==============================================================================

@app.route("/usuarios/listar")
def listagem_usuarios():
    return render_template("usuarios/listagem_usuarios.html")


@app.route("/usuarios/inserir")
def cadastro_usuarios():
    return render_template("usuarios/cadastro_usuarios.html")

# ==============================================================================
# VENDAS
# ==============================================================================

@app.route("/vendas/listar")
def listagem_vendas():
    return render_template("vendas/listagem_vendas.html")


@app.route("/vendas/inserir")
def cadastro_vendas():
    return render_template("vendas/cadastro_vendas.html")

# ==============================================================================
# PERFIL
# ==============================================================================

@app.route("/perfis/inserir", methods=["GET", "POST"])
def inserir_perfil():

    nome = ""
    descricao = ""

    if request.method == "POST":
        nome = request.form.get("nome").strip()
        descricao = request.form.get("descricao").strip()

    try:
        novo_id = execute_insert(
           'INSERT INTO perfis (nome, descricao) VALUES(%s,%s)',
           (nome, descricao)
        )
        flash(f"Perfil {nome} cadastro com o ID: {novo_id}", "success")
        return redirect(url_for("listar_perfis"))

    except Error as erro:
        if erro.errno == 1062:
            flash("Já existe um perfil com este nome", "danger")
        else:
            raise

    return render_template("perfis/perfil-form.html", nome=nome, descricao=descricao)

@app.route("/perfis")
def listar_perfis():
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
        fetch=True
    )

    return render_template("perfis/perfis-listar.html", perfis=perfis)












# ==============================================================================
# TELAS DE ERROS
# ==============================================================================

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('404.html'), 404


@app.errorhandler(500)
def erro_no_servidor(erro):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)
