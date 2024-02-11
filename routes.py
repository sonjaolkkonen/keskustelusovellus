from app import app
from flask import render_template, request, redirect, session, abort
import users, topics, messages, comments


@app.route("/")
def index():
    user_is_admin = users.is_admin()
    topics_list = topics.get_list()
    messages_list = messages.get_list()
    return render_template("index.html", user_is_admin = user_is_admin, topics = topics_list, messages = messages_list)

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
    
@app.route("/create_topic", methods=["POST"])
def create_topic():
    check_csrf_token()
    topic = request.form["topic"]
    if topics.create_topic(topic):
        return redirect("/")
    
@app.route("/chat/<message_id>")
def chat(message_id):
    message_id = message_id
    message_thread = messages.get_thread(message_id)
    message_comments = comments.get_comments(message_id)
    return render_template("chat.html", thread = message_thread, comments = message_comments)

@app.route("/new")
def new():
    topics_list = topics.get_list()
    return render_template("new.html", topics = topics_list)

@app.route("/send", methods=["POST"])
def send():
    check_csrf_token()
    headline = request.form["headline"]
    topic = request.form["topic"]
    content = request.form["content"]
    if messages.send(topic, content, headline):
        return redirect("/")
    else:
        return render_template("error.html", message="Viestin lähetys ei onnistunut.")

@app.route("/new_comment/<message_id>")
def new_comment(message_id):
    message_id = message_id
    return render_template("new_comment.html", message_id=message_id)

@app.route("/send_comment", methods=["POST"])
def send_comment():
    check_csrf_token()
    content = request.form["content"]
    message_id = request.form["message_id"]
    if comments.send(content, message_id):
        message_thread = messages.get_thread(message_id)
        message_comments = comments.get_comments(message_id)
        return render_template("chat.html", thread = message_thread, comments = message_comments)
    else:
        return render_template("error.html", message="Kommentin lisääminen ei onnistunut.")
    
@app.route("/filter_by_topic/<topic>")
def filter_by_topic(topic):
    topic = topic
    if topic == "None":
        return redirect("/")
    user_is_admin = users.is_admin()
    filter_result = messages.filter_by_topic(topic)
    return render_template("filter_by_topic.html", user_is_admin = user_is_admin, messages = filter_result)


def check_csrf_token():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
