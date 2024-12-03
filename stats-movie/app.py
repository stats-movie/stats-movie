from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "rochakkj."
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/cadastro", methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user
        return redirect(url_for("login"))
    else:
        return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        username = session["user"]
        return f"<h1>Ola {username}</h1>"
    else:
        return redirect(url_for("cadastro"))
    
@app.route("/logout")
def logout():
    if "user" in session:
        username = session["user"]
        flash(f"Usuário, {username}, deslogado com sucesso!", "info")
    session.pop("user", None)
    return redirect(url_for("cadastro"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)