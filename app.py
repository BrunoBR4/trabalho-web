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
            return redirect(url_for("dashboard"))

    return render_template(
        "login.html",
        erro_email=erro_email,
        erro_senha=erro_senha,
        email_digitado=email_digitado,
    )


# Página provisória, só para mostrar o nome do usuário logado.
@app.route("/dashboard")
def dashboard():
    if "nome" not in session:  # quem não fez login volta para a tela inicial
        return redirect(url_for("login"))
    return render_template("dashboard.html", nome=session["nome"])


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
