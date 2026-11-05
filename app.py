from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True)
