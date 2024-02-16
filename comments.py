import locale
from sqlalchemy.sql import text
from flask import session
from db import db
import users

def get_comments(message_id):
    user_id = users.user_id()
    sql = text("""SELECT C.content, U.username, C.sent_at, C.id, C.user_id, C.up_votes, C.down_votes
               FROM comments C, users U WHERE C.message_id=:message_id
               AND U.id=C.user_id AND C.visible=1 ORDER BY C.sent_at ASC""")
    result = db.session.execute(sql, {"user":user_id, "message_id":message_id})
    return result.fetchall()

def get_amount_of_comments():
    sql = text("""SELECT message_id, COUNT(message_id) FROM comments
               WHERE visible=1 GROUP BY message_id""")
    result = db.session.execute(sql)
    return result.fetchall()

def get_comment_time():
    locale.setlocale(locale.LC_TIME, 'fi_FI.UTF-8')
    sql = text("""SELECT message_id, sent_at FROM comments
               WHERE id IN (SELECT MAX(id) FROM comments
               WHERE visible=1 GROUP BY message_id)""")
    result = db.session.execute(sql)
    return result.fetchall()

def send(content, message_id):
    user_id = users.user_id()
    if user_id is None:
        return False
    sql = text("""INSERT INTO comments (content, user_id, message_id, sent_at,
               visible, up_votes, down_votes)
               VALUES (:content, :user_id, :message_id, NOW(), 1, 0, 0)""")
    db.session.execute(sql, {"content":content, "user_id":user_id, "message_id":message_id})
    db.session.commit()
    return True

def delete_comment(comment_id):
    if users.is_admin() or is_users_comment(comment_id):
        sql = text("UPDATE comments SET visible=0 WHERE id=:comment_id")
        db.session.execute(sql, {"comment_id":comment_id})
        db.session.commit()
        return True
    return False

def edit_comment(comment_id, edit):
    if is_users_comment(comment_id):
        sql = text("UPDATE comments SET content=:edit WHERE id=:comment_id")
        db.session.execute(sql, {"edit":edit, "comment_id":comment_id})
        db.session.commit()
        return True
    return False

def is_users_comment(comment_id):
    user_id = users.user_id()
    sql = text("""SELECT id, content, user_id, message_id, sent_at FROM comments
               WHERE user_id=:user_id AND id=:comment_id""")
    result = db.session.execute(sql, {"user_id":user_id, "comment_id":comment_id})
    if result.fetchone():
        return True
    return False

def vote_comment(vote, comment_id):
    user_id = users.user_id()
    has_voted = users.check_if_voted_comment(user_id, comment_id)
    if user_id == 0 or has_voted:
        return False

    if vote == -1:
        try:
            sql = text("UPDATE comments SET down_votes=down_votes+1 WHERE id=:comment_id")
            db.session.execute(sql, {"comment_id":comment_id})
            db.session.commit()
            users.has_voted_comment(user_id, comment_id)
            return True
        except:
            return False

    elif vote == 1:
        try:
            sql = text("UPDATE comments SET up_votes=up_votes+1 WHERE id=:comment_id")
            db.session.execute(sql, {"comment_id":comment_id})
            db.session.commit()
            users.has_voted_comment(user_id, comment_id)
            return True
        except:
            return False
