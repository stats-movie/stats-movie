from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from funcs_db import usuario_inserir, usuario_checar, usuario_listar, criar_database
import mysql.connector  
app = Flask(__name__)
app.secret_key = "rochakkj."
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return redirect(url_for("homepage"))

@app.route("/cadastro", methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        criar_database()
        nome_usuario = request.form['username']
        email = request.form['email']
        senha = request.form['password']
        nome = f"{request.form['nome']} {request.form['sobrenome']}"
        try:
            usuario_inserir(nome_usuario, email, senha, nome)
        except mysql.connector.IntegrityError:
            flash(f"Este Nome de Usuário ou Email já foi utilizado!", "info")
            return redirect(url_for("cadastro"))
        return redirect(url_for("login"))
    else:
        return render_template("cadastro.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if "user" in session:
        return redirect(url_for("user"))

    if request.method == "POST":
        usuario = request.form["user"]
        senha = request.form["password"]
        tipo = "nome_usuario"
        for i in list(usuario):
            if i == '@':
                tipo = "email"

        if usuario_checar(usuario, tipo, senha) == usuario:
            session.permanent = True
            session['user'] = usuario_listar(usuario, tipo, "nome_usuario")
            session['email'] = usuario_listar(usuario, tipo, "email")
            session['nome'] = usuario_listar(usuario, tipo, "nome")
            return redirect(url_for("user"))
        flash(f"Usuário, email ou senha não encontrado!", "info")
    return render_template("login.html")

@app.route("/homepage")
def homepage():

    return render_template("homepage.html")

@app.route("/user")
def user():
    if "user" in session:  
        return f"<h1>Ola seu nome de usuario é {session['user']}! <br> Seu email é {session['email']} <br> Seu nome é {session['nome']}</h1>"
    else:
        return redirect(url_for("login"))
    
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