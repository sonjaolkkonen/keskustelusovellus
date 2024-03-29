CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    headline TEXT,
    content TEXT,
    user_id INTEGER REFERENCES users,
    topic_id INTEGER REFERENCES topics,
    sent_at TIMESTAMP,
    visible INTEGER,
    up_votes INTEGER,
    down_votes INTEGER
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    message_id INTEGER REFERENCES messages,
    sent_at TIMESTAMP,
    visible INTEGER,
    up_votes INTEGER,
    down_votes INTEGER
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    message_id INTEGER REFERENCES messages,
    comment_id INTEGER REFERENCES comments
);