from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "rochakkj."

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/cadastro", methods = ["POST", "GET"])
def cadastro():
    if request.method == "POST":
        return redirect(url_for("home"))
    else:
        return render_template("cadastro.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)