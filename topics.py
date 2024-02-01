from sqlalchemy.sql import text
from db import db
import users

def get_list():
    sql = text("SELECT name FROM topics ORDER BY name")
    result = db.session.execute(sql)
    return result.fetchall()

def create_topic(topic):
    user_id = users.user_id
    if user_id == 0:
        return False
    sql = text("INSERT INTO topics (name) VALUES (:name)")
    db.session.execute(sql, {"name":topic})
    db.session.commit()
    return True

def get_id(topic_name):
    sql = text("SELECT id FROM topics WHERE name=:topic_name")
    result = db.session.execute(sql, {"topic_name":topic_name})
    topic_id = result.fetchone()
    print(topic_id)
    if not topic_id:
        return False
    else:
        return topic_id[0]