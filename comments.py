from sqlalchemy.sql import text
from db import db
from flask import session
import users

def get_comments(message_id):
    user_id = users.user_id()
    sql = text("SELECT C.content, U.username, C.sent_at, C.id, C.user_id FROM comments C, users U WHERE C.message_id=:message_id AND U.id=C.user_id ORDER BY C.sent_at ASC")
    result = db.session.execute(sql, {"user":user_id, "message_id":message_id})
    return result.fetchall()

def send(content, message_id):
    user_id = users.user_id()
    if user_id == None:
        return False
    sql = text("INSERT INTO comments (content, user_id, message_id, sent_at) VALUES (:content, :user_id, :message_id, NOW())")
    db.session.execute(sql, {"content":content, "user_id":user_id, "message_id":message_id})
    db.session.commit()
    return True



