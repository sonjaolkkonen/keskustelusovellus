from sqlalchemy.sql import text
from db import db
import messages, comments, users

def get_message_up_votes(message_id):
    sql = text("SELECT up_votes FROM votes WHERE message_id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id}).fetchall()
    up_votes = 0
    for vote in result:
        if vote[0] != None:
            up_votes += vote[0]
    return up_votes

def get_message_down_votes(message_id):
    sql = text("SELECT down_votes FROM votes WHERE message_id=:message_id")
    result = db.session.execute(sql, {"message_id":message_id}).fetchall()
    down_votes = 0
    for vote in result:
        if vote[0] != None:
            down_votes += vote[0]
    return down_votes

# def get_comment_up_votes(comment_id):
#     sql = text("SELECT up_votes FROM votes WHERE comment_id=:comment_id")
#     result = db.session.execute(sql, {"comment_id":comment_id})
#     return result.fetchone()

# def get_comment_down_votes(comment_id):
#     sql = text("SELECT down_votes FROM votes WHERE comment_id=:comment_id")
#     result = db.session.execute(sql, {"comment_id":comment_id})
#     return result.fetchone()

def send_message_vote(vote, message_id):
    user_id = users.user_id()
    if user_id == 0:
        return False

    if vote == -1:
        try:
            sql = text("INSERT INTO votes (down_votes, all_votes, user_id, message_id) VALUES (1, 1, :user_id, :message_id)")
            db.session.execute(sql, {"user_id":user_id, "message_id":message_id})
            db.session.commit()
            return True
        except:
            return False
            
    elif vote == 1:
        try:
            sql = text("INSERT INTO votes (up_votes, all_votes, user_id, message_id) VALUES (1, 1, :user_id, :message_id)")
            db.session.execute(sql, {"user_id":user_id, "message_id":message_id})
            db.session.commit()
            return True
        except:
            return False
    
