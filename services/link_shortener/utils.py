import sqlite3
import string
import random
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''
    CREATE TABLE IF NOT EXISTS links
    (id TEXT PRIMARY KEY, original_url TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    db.commit()

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(chars) for _ in range(length))
    return short_id