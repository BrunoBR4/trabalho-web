from flask import Flask, render_template

app = Flask(__name__)


# Rota da página de login.
# "/" é o endereço inicial do site, então o login será a primeira tela.
# methods=["GET", "POST"]: GET abre a página, POST recebe o formulário.
# Por enquanto só mostramos a página; a verificação do usuário vem depois.
@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)    