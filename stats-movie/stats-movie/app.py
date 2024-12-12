from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from funcs_db import usuario_inserir, usuario_checar, usuario_listar, criar_database
import mysql.connector
from hasher import senha_hash

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
        nome = f"{request.form['nome'].strip()} {request.form['sobrenome'].strip()}"
        nome_usuario = request.form['username'].strip()
        email = request.form['email'].strip()
        senha = request.form['password'].strip()
        hash = senha_hash(senha)
        try:
            usuario_inserir(nome_usuario, email, hash, nome)
        except mysql.connector.IntegrityError:
            flash(f"Este Nome de Usuário ou Email já foi utilizado!", "info")
            return redirect(url_for("cadastro"))
        return redirect(url_for("login"))
    else:
        return render_template("cadastro.html")

@app.route("/login", methods = ["POST", "GET"])
def login():
    if "user" in session:
        return redirect(url_for("perfil"))

    if request.method == "POST":
        usuario = request.form["user"].strip()
        senha = request.form["password"]
        resultado = usuario_checar(usuario, senha)
        if resultado == 0:
            session.permanent = True
            session['user'] = usuario_listar(usuario, "nome_usuario")
            session['email'] = usuario_listar(usuario, "email")
            session['nome'] = usuario_listar(usuario, "nome")
            return redirect(url_for("perfil"))
        
        elif resultado == 1:
            flash(f"Usuário ou email não encontrado!", "info")

        elif resultado == 2:
            flash(f"Senha incorreta!", "info")

    return render_template("login.html")

@app.route("/homepage")
def homepage():

    return render_template("homepage.html")

@app.route("/user")
def user():
    return redirect(url_for("perfil"))

@app.route("/perfil")
def perfil():
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
    session.pop("email", None)
    session.pop("nome", None)
    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)