from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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

# == PADRONIZAÇÃO !!!!! ==

@app.route("/", methods=["GET", "POST"])
def inicio():
        return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", anuncios=ANUNCIOS)


@app.route("/usuarios/listar")
def listagem_usuarios():
    return render_template("usuarios/listagem_usuarios.html")


@app.route("/usuarios/inserir")
def cadastro_usuarios():
    return render_template("usuarios/cadastro_usuarios.html")


@app.route("/vendas/listar")
def listagem_vendas():
    return render_template("vendas/listagem_vendas.html")


@app.route("/vendas/inserir")
def cadastro_vendas():
    return render_template("vendas/cadastro_vendas.html")


@app.route("/sair")
def sair():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
