from sqlalchemy.sql import text
from db import db
from flask import session
import users

def get_comments(message_id):
    user_id = users.user_id()
    sql = text("SELECT C.content, U.username, C.sent_at, C.id, C.user_id FROM comments C, users U WHERE C.message_id=:message_id AND U.id=C.user_id AND C.visible=1 ORDER BY C.sent_at ASC")
    result = db.session.execute(sql, {"user":user_id, "message_id":message_id})
    return result.fetchall()

def send(content, message_id):
    user_id = users.user_id()
    if user_id == None:
        return False
    sql = text("INSERT INTO comments (content, user_id, message_id, sent_at, visible) VALUES (:content, :user_id, :message_id, NOW(), 1)")
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
    sql = text("SELECT id, content, user_id, message_id, sent_at FROM comments WHERE user_id=:user_id AND id=:comment_id")
    result = db.session.execute(sql, {"user_id":user_id, "comment_id":comment_id})
    if result.fetchone() != None:
        return True
    else:
        return False
