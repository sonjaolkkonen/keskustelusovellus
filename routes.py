from app import app
from flask import render_template, request, redirect
import users


@app.route("/")
def index():
    user_is_admin = users.is_admin()
    return render_template("index.html", user_is_admin=user_is_admin)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Antamasi käyttäjätunnus tai salasana on väärä.")
        
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        admin = int(request.form["admin"])
        if password1 != password2:
            return render_template("error.html", message="Antamasi salasanat eivät täsmää.")
        if users.register(username, password1, admin):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut.")
        
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/topic")
def topic():
    user_is_admin = users.is_admin()
    if users.user_id() and user_is_admin:
        return render_template("topic.html", user_is_admin = user_is_admin)
    else:
        return redirect("/")