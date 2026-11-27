import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for, request, flash, abort
from flask_wtf.csrf import CSRFProtect

from db import execute_one, execute_query, execute_insert

from mysql.connector import Error

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CSRFProtect(app)

# ==============================================================================
# PÁGINAS PRINCIPAIS
# ==============================================================================

@app.route("/", methods=["GET", "POST"])
def inicio():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

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

    return render_template("perfis/perfil-form.html", nome=nome, descricao=descricao, acao='inserir')

@app.route("/perfis")
def listar_perfis():
    perfis = execute_query(
        'SELECT id_perfil, nome, descricao, criado_em FROM perfis ORDER BY nome',
        fetch=True
    )

    return render_template("perfis/perfis-listar.html", perfis=perfis)

@app.route("/perfis/<int:id_perfil>/editar", methods=["GET", "POST"])
def editar_perfil(id_perfil):
    perfil = execute_one(
        'SELECT id_perfil, nome, descricao FROM perfis WHERE id_perfil = %s',
        (id_perfil,),
    )

    if perfil is None:
        abort(404)

    nome = perfil['nome'],
    descricao = perfil['descricao']

    if request.method == 'POST':
        nome = request.form.get('nome').strip()
        descricao = request.form.get('descricao').strip()

        try:
            execute_query('''
                UPDATE perfis SET
                    nome = %s,
                    descricao=%s
                WHERE id_perfil = %s
                         ''',
                         (nome, descricao, id_perfil)
                         )
            return redirect(url_for('listar_perfis'))
        except Error as erro:
                if erro.errno == 1062:
                    flash("Já existe um perfil com este nome", "danger")
                else:
                    raise

    return render_template("perfis/perfil-form.html", id_perfil=id_perfil, nome=nome, descricao=descricao, acao='editar')

@app.route("/perfis/<int:id_perfil>/excluir", methods=["POST"])
def excluir_perfil(id_perfil):
    perfil = execute_one(
            'SELECT id_perfil, nome, descricao FROM perfis WHERE id_perfil = %s',
            (id_perfil,),
        )
    
    if perfil is None:
            abort(404)

    try:
        execute_query('DELETE FROM perfis WHERE id_perfil = %s',
                      (id_perfil,))
        flash(f'O perfil {perfil["nome"]} foi excluído!', 'danger')
    except Error as erro:
            if erro.errno == 1451:
                flash('PERFIL NÃO PODE SER EXCLUÍDO!', 'danger')
            else:
                raise
    return redirect(url_for('listar_perfis'))

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
