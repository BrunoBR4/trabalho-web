from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# O Flask usa esta chave para guardar com segurança o "session" (a memória do login).
app.secret_key = "meetcars-chave-secreta"

# "Banco de dados" simulado: um dicionário onde a chave é o e-mail
# e o valor é outro dicionário com o nome e a senha do usuário.
USUARIOS = {
    "brunowantonio1@gmail.com": {"nome": "Bruno", "senha": "12345"},
    "meuemail@gmail.com": {"nome": "Ronan", "senha": "1234"},
}

# Anúncios de venda da página Comércio (dados fictícios, só para a apresentação).
# Cada anúncio é um dicionário. Para mudar um anúncio, edite os valores aqui.
ANUNCIOS = [
    {"modelo": "Skyline GT-R R34", "marca": "Nissan", "ano": 1999,
     "km": "58.000", "preco": "R$ 950.000,00"},
    {"modelo": "X3 M40i", "marca": "BMW", "ano": 2019,
     "km": "41.500", "preco": "R$ 289.900,00"},
    {"modelo": "Corolla XEi", "marca": "Toyota", "ano": 2021,
     "km": "32.000", "preco": "R$ 128.900,00"},
    {"modelo": "Civic Touring", "marca": "Honda", "ano": 2020,
     "km": "45.300", "preco": "R$ 139.900,00"},
    {"modelo": "Compass Limited", "marca": "Jeep", "ano": 2022,
     "km": "24.800", "preco": "R$ 169.900,00"},
    {"modelo": "Mustang GT", "marca": "Ford", "ano": 2018,
     "km": "36.200", "preco": "R$ 349.000,00"},
]


@app.route("/", methods=["GET", "POST"])
def login():
    erro_email = None
    erro_senha = None
    email_digitado = ""

    # POST = o formulário foi enviado (clicou em "Entrar")
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        usuario = USUARIOS.get(email)  # procura o e-mail no dicionário

        if usuario is None:
            # E-mail não existe no dicionário
            erro_email = "E-mail desconhecido!"
        elif usuario["senha"] != senha:
            # E-mail existe, mas a senha não confere
            erro_senha = "Senha incorreta!"
            email_digitado = email  # mantém o e-mail para não digitar de novo
        else:
            # Tudo certo: guarda o nome na sessão e vai para a próxima página
            session["nome"] = usuario["nome"]
            return redirect(url_for("comercio"))

    return render_template(
        "login.html",
        erro_email=erro_email,
        erro_senha=erro_senha,
        email_digitado=email_digitado,
    )


# Cadastro aberto (sem menu lateral): quem chega pelo botão "Cadastrar" do login.
# Não exige login, por isso não verifica a sessão.
@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


# ===== Páginas com menu lateral =====
# Em cada uma, quem não fez login (sem "nome" na sessão) volta para o login.
# O nome do usuário aparece no menu direto pelo template, via session.

@app.route("/comercio")
def comercio():
    if "nome" not in session:
        return redirect(url_for("login"))
    return render_template("comercio.html", anuncios=ANUNCIOS)


@app.route("/usuarios")
def listagem_usuarios():
    if "nome" not in session:
        return redirect(url_for("login"))
    return render_template("listagem_usuarios.html")


@app.route("/usuarios/cadastro")
def cadastro_usuarios():
    if "nome" not in session:
        return redirect(url_for("login"))
    return render_template("cadastro_usuarios.html")


@app.route("/vendas")
def listagem_vendas():
    if "nome" not in session:
        return redirect(url_for("login"))
    return render_template("listagem_vendas.html")


@app.route("/vendas/cadastro")
def cadastro_vendas():
    if "nome" not in session:
        return redirect(url_for("login"))
    return render_template("cadastro_vendas.html")


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
