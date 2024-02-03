from sqlalchemy.sql import text
from db import db
import users, topics

def get_list():
    sql = text("SELECT M.id, M.headline, M.content, U.username, M.sent_at, T.name FROM messages M, users U, topics T WHERE M.user_id=U.id AND M.topic_id = T.id ORDER BY M.id")
    result = db.session.execute(sql)
    return result.fetchall()

def send(topic, content, headline):
    user_id = users.user_id()
    topic_id = topics.get_id(topic)
    if user_id == 0:
        return False
    sql = text("INSERT INTO messages (headline, content, user_id, topic_id, sent_at) VALUES (:headline, :content, :user_id, :topic_id, NOW())")
    db.session.execute(sql, {"headline":headline, "content":content, "user_id":user_id, "topic_id":topic_id})
    db.session.commit()
    return True

def get_thread(message_id):
    sql = text("SELECT headline, content, sent_at FROM messages WHERE id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id})
    message_thread = result.fetchall()
    return message_thread