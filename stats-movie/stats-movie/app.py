from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from funcs_db import usuario_inserir, usuario_checar, usuario_listar, usuario_atualizar, criar_database
import mysql.connector
from hasher import senha_hash

app = Flask(__name__)
app.secret_key = "rochakkj."
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/homepage")
def homepage():
    if "user" in session:
        return render_template("homepage.html")
    flash("Para acessar o sistema é necessário estar logado!", "info")
    return redirect(url_for("login"))

@app.route("/home")
def home():
    return redirect(url_for("homepage"))    

@app.route("/", methods = ["POST", "GET"])
def landingpage():
    if request.method == "POST":
        if "user" in session:
            return redirect(url_for("homepage"))
        else:
            flash("Para acessar o sistema é necessário estar logado!", "info")
            return redirect(url_for("login"))
    return render_template("landingpage.html")


@app.route("/cadastro", methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        criar_database()
        nome = f"{request.form['nome'].strip()} {request.form['sobrenome']}"
        nome_usuario = request.form['username'].strip()
        email = request.form['email'].strip()
        senha = request.form['password']
        #senha_confirm = request.form['password-confirm']
        #if(senha != senha_confirm):
        #        flash("Senhas não correspondentes!", "warning")
        #        return redirect(url_for("cadastro"))
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
            session['nome'] = (usuario_listar(usuario, "nome")).split(" ")[0]
            session['sobrenome'] = (usuario_listar(usuario, "nome")).split(" ")[-1]
            if (usuario_listar(usuario, "foto_perfil") != None):
                session['foto-perfil'] = (usuario_listar(usuario, "foto_perfil"))
            if (usuario_listar(usuario, "numero_celular") != None):
                session['celular'] = (usuario_listar(usuario, "numero_celular"))
            if (usuario_listar(usuario, "data_nascimento") != None):
                data = (usuario_listar(usuario, "data_nascimento"))
                session['data'] = data.strftime("%Y-%d-%m")
            return redirect(url_for("homepage"))
        
        elif resultado == 1:
            flash(f"Usuário ou email não encontrado!", "info")

        elif resultado == 2:
            flash(f"Senha incorreta!", "info")

    return render_template("login.html")


@app.route("/user")
def user():
    return redirect(url_for("perfil"))

@app.route("/perfil", methods = ["POST", "GET"])
def perfil():
    if "user" in session:
        if request.method == "POST":
            nome_usuario_antigo = session["user"]
            nome = f"{request.form['nome'].strip()} {request.form['sobrenome'].strip()}"
            nome_usuario = request.form['username'].strip()
            email = request.form['email'].strip()
            senha = request.form['password']
            if senha != "":
                senha_confirm = request.form['password-confirm']
                if(senha != senha_confirm):
                    flash("Senhas não correspondentes!", "warning")
                    return redirect(url_for("perfil"))
                senha = senha_hash(senha)
            data_nascimento = request.form['data-nascimento']
            numero_celular = request.form['numero-celular']
            foto_perfil = request.form['foto-perfil']
            usuario_atualizar(nome_usuario_antigo, nome_usuario, email, senha, nome, data_nascimento, numero_celular, foto_perfil)
            session["user"] = nome_usuario
            session["email"] = email
            session["nome"] = request.form['nome']
            session["sobrenome"] = request.form['sobrenome']
            session["data"] = data_nascimento
            session["celular"] = numero_celular
            session["foto-perfil"] = foto_perfil
            return redirect(url_for("home"))
        else:
            return render_template("perfil.html")
        
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
    session.pop("sobrenome", None)
    session.pop("data", None)
    session.pop("celular", None)
    session.pop("foto-perfil", None)

    return redirect(url_for("login"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)