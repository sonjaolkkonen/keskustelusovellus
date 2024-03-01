from flask import render_template, request, redirect, session, abort, flash, url_for
from app import app
import users
import topics
import messages
import comments


@app.route("/")
def index():
    user_is_admin = users.is_admin()
    topics_list = topics.get_list()
    messages_list = messages.get_list()
    amount_of_comments = comments.get_amount_of_comments()
    times = comments.get_comment_time()
    return render_template("index.html", user_is_admin = user_is_admin, topics = topics_list,
                           messages = messages_list, comments=amount_of_comments, times=times)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html",
                                message="Antamasi käyttäjätunnus tai salasana on väärä.")

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
    return redirect("/")

@app.route("/create_topic", methods=["POST"])
def create_topic():
    check_csrf_token()
    new_topic = request.form["topic"]
    if topics.create_topic(new_topic):
        return redirect("/")

@app.route("/chat/<message_id>")
def chat(message_id):
    message_thread = messages.get_thread(message_id)
    message_comments = comments.get_comments(message_id)
    user_is_admin = users.is_admin()
    return render_template("chat.html", thread = message_thread,
                           comments = message_comments, user_is_admin = user_is_admin)

@app.route("/new")
def new():
    topics_list = topics.get_list()
    return render_template("new.html", topics = topics_list)

@app.route("/send", methods=["POST"])
def send():
    check_csrf_token()
    headline = request.form["headline"]
    message_topic = request.form["topic"]
    content = request.form["content"]
    if messages.send(message_topic, content, headline):
        return redirect("/")
    return render_template("error.html", message="Viestin lähetys ei onnistunut.")

@app.route("/new_comment/<message_id>")
def new_comment(message_id):
    return render_template("new_comment.html", message_id=message_id)

@app.route("/send_comment", methods=["POST"])
def send_comment():
    check_csrf_token()
    content = request.form["content"]
    message_id = request.form["message_id"]
    if comments.send(content, message_id):
        return redirect(url_for("chat", message_id=message_id))
    return render_template("error.html", message="Kommentin lisääminen ei onnistunut.")

@app.route("/filter_by_topic/<topic>")
def filter_by_topic(topic):
    if topic == "None":
        return redirect("/")
    user_is_admin = users.is_admin()
    filter_result = messages.filter_by_topic(topic)
    if filter_result == []:
        return render_template("error.html", message="Ei vielä aloitettuja keskusteluita.")
    return render_template("filter_by_topic.html",
                            user_is_admin = user_is_admin, messages = filter_result)

@app.route("/search")
def search():
    query = request.args["query"]
    user_is_admin = users.is_admin()
    search_result = messages.search(query)
    return render_template("search.html", messages=search_result, user_is_admin=user_is_admin)

@app.route("/remove_message/<message_id>")
def remove_message(message_id):
    if messages.delete_message(message_id):
        return redirect("/")

@app.route("/remove_comment/<comment_id>")
def remove_comment(comment_id):
    if comments.delete_comment(comment_id):
        flash("Viesti poistettu")
        return redirect(request.referrer)

@app.route("/edit_comment/<message_id>/<comment_id>/<content>")
def edit_comment(comment_id, message_id, content):
    return render_template("edit_comment.html", comment_id=comment_id, message_id=message_id, content=content)

@app.route("/send_comment_edit", methods=["POST"])
def send_comment_edit():
    check_csrf_token()
    edit = request.form["content"]
    comment_id = request.form["comment_id"]
    message_id = request.form["message_id"]
    if comments.edit_comment(comment_id, edit):
        return redirect(url_for("chat", message_id=message_id))
    return render_template("error.html", message="Kommentin muokkaaminen ei onnistunut.")

@app.route("/edit_message/<message_id>/<content>")
def edit_message(message_id, content):
    return render_template("edit_message.html", message_id=message_id, content=content)

@app.route("/edit_headline/<message_id>/<headline>")
def edit_headline(message_id, headline):
    return render_template("edit_headline.html", message_id=message_id, headline=headline)

@app.route("/send_headline_edit", methods=["POST"])
def send_headline_edit():
    check_csrf_token()
    edit = request.form["headline"]
    message_id = request.form["message_id"]
    if messages.edit_headline(message_id, edit):
        return redirect(url_for("chat", message_id=message_id))
    return render_template("error.html", message="Otsikon muokkaaminen ei onnistunut.")

@app.route("/send_message_edit", methods=["POST"])
def send_message_edit():
    check_csrf_token()
    edit = request.form["content"]
    message_id = request.form["message_id"]
    if messages.edit_message(message_id, edit):
        return redirect(url_for("chat", message_id=message_id))
    return render_template("error.html", message="Viestin muokkaaminen ei onnistunut.")

@app.route("/up_vote_message/<message_id>")
def up_vote(message_id):
    if messages.vote_message(1, message_id):
        return redirect(request.referrer)
    flash("Olet jo äänestänyt tai et ole kirjautunut sisään")
    return redirect(request.referrer)

@app.route("/down_vote_message/<message_id>")
def down_vote(message_id):
    if messages.vote_message(-1, message_id):
        return redirect(request.referrer)
    flash("Olet jo äänestänyt tai et ole kirjautunut sisään")
    return redirect(request.referrer)

@app.route("/up_vote_comment/<comment_id>")
def up_vote_comment(comment_id):
    if comments.vote_comment(1, comment_id):
        return redirect(request.referrer)
    flash("Olet jo äänestänyt tai et ole kirjautunut sisään")
    return redirect(request.referrer)

@app.route("/down_vote_comment/<comment_id>")
def down_vote_comment(comment_id):
    if comments.vote_comment(-1, comment_id):
        return redirect(request.referrer)
    flash("Olet jo äänestänyt tai et ole kirjautunut sisään")
    return redirect(request.referrer)

def check_csrf_token():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
