from sqlalchemy.sql import text
from db import db
import users
import topics

def get_list():
    sql = text("""SELECT M.id, M.headline, M.content, U.username, M.sent_at,
               T.name, M.up_votes, M.down_votes
               FROM messages M, users U, topics T
               WHERE M.user_id=U.id AND M.topic_id = T.id AND M.visible=1 ORDER BY M.id""")
    result = db.session.execute(sql)
    return result.fetchall()

def send(topic, content, headline):
    user_id = users.user_id()
    topic_id = topics.get_id(topic)
    if user_id == 0:
        return False
    try:
        sql = text("""INSERT INTO messages (headline, content, user_id, topic_id,
                   sent_at, visible, up_votes, down_votes)
                   VALUES (:headline, :content, :user_id, :topic_id, NOW(), 1, 0, 0)""")
        db.session.execute(sql, {"headline":headline, "content":content,
                                 "user_id":user_id, "topic_id":topic_id})
        db.session.commit()
        return True
    except:
        return False

def get_thread(message_id):
    sql = text("""SELECT id, headline, content, sent_at, user_id, up_votes, down_votes
               FROM messages WHERE id=:message_id AND visible=1""")
    result = db.session.execute(sql, {"message_id":message_id})
    message_thread = result.fetchall()
    return message_thread

def filter_by_topic(topic):
    sql = text("""SELECT M.id, M.headline, M.content, M.user_id, M.sent_at, T.name, U.username,
               M.up_votes, M.down_votes
               FROM messages M, topics T, users U
               WHERE M.user_id=U.id AND M.topic_id=T.id AND T.name=:topic AND M.visible=1
               ORDER BY M.id""")
    result = db.session.execute(sql, {"topic":topic})
    filter_result = result.fetchall()
    return filter_result

def search(query):
    sql = text("""SELECT M.id, M.headline, M.content, M.user_id, M.sent_at, T.name, U.username,
               M.up_votes, M.down_votes
               FROM messages M, topics T, users U
               WHERE M.user_id=U.id AND M.topic_id=T.id AND
               (M.content iLIKE :query OR M.headline iLIKE :query OR M.id IN
               (SELECT C.message_id FROM comments C WHERE C.content iLike :query AND C.visible=1))
               AND M.visible=1 ORDER BY M.id""")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    search_result = result.fetchall()
    return search_result

def delete_message(message_id):
    if users.is_admin() or is_users_message(message_id):
        sql = text("UPDATE messages SET visible=0 WHERE id=:message_id")
        db.session.execute(sql, {"message_id":message_id})
        db.session.commit()
        return True

    return False

def edit_message(message_id, edit):
    if is_users_message(message_id):
        sql = text("UPDATE messages SET content=:edit WHERE id=:message_id")
        db.session.execute(sql, {"edit":edit, "message_id":message_id})
        db.session.commit()
        return True
    return False

def edit_headline(message_id, edit):
    if is_users_message(message_id):
        sql = text("UPDATE messages SET headline=:edit WHERE id=:message_id")
        db.session.execute(sql, {"edit":edit, "message_id":message_id})
        db.session.commit()
        return True
    return False

def is_users_message(message_id):
    user_id = users.user_id()
    sql = text("""SELECT id, headline, content, user_id, topic_id, sent_at
               FROM messages WHERE user_id=:user_id AND id=:message_id""")
    result = db.session.execute(sql, {"user_id":user_id, "message_id":message_id})
    if result.fetchone():
        return True
    return False

def vote_message(vote, message_id):
    user_id = users.user_id()
    has_voted = users.check_if_voted(user_id, message_id)
    if user_id == 0 or has_voted:
        return False

    if vote == -1:
        try:
            sql = text("UPDATE messages SET down_votes=down_votes+1 WHERE id=:message_id")
            db.session.execute(sql, {"message_id":message_id})
            db.session.commit()
            users.has_voted(user_id, message_id)
            return True
        except:
            return False

    elif vote == 1:
        try:
            sql = text("UPDATE messages SET up_votes=up_votes+1 WHERE id=:message_id")
            db.session.execute(sql, {"message_id":message_id})
            db.session.commit()
            users.has_voted(user_id, message_id)
            return True
        except:
            return False
        