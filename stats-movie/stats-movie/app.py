from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from funcs_db import usuario_inserir, usuario_checar, usuarios_listar

app = Flask(__name__)
app.secret_key = "rochakkj."
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/cadastro", methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        nome_usuario = request.form['username']
        email = request.form['email']
        senha = request.form['password']
        usuario_inserir(nome_usuario, email, senha)
        return redirect(url_for("login"))
    else:
        return render_template("cadastro.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        usuario = request.form["user"]
        if usuario_checar(usuario, "nome_usuario") == usuario:
            session.permanent = True
            session["user"] = usuario
            senha = request.form["password"]
            session["password"] = senha
            return redirect(url_for("user"))
        flash(f"Usuário/email, {usuario}, não encontrado!", "info")
    return render_template("login.html")

@app.route("/homepage")
def homepage():

    return render_template("homepage.html")

@app.route("/user")
def user():
    if "user" in session:
        username = session["user"]
        return f"<h1>Ola {username}!</h1>"
    else:
        return redirect(url_for("cadastro"))
    
@app.route("/logout")
def logout():
    if "user" in session:
        username = session["user"]
        flash(f"Usuário, {username}, deslogado com sucesso!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)