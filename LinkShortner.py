from flask import Flask, request, redirect, render_template
import sqlite3
import string
import random
from urllib.parse import urlparse
import os.path

app = Flask(__name__)


# Setup database
def init_db():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS links
    (id TEXT PRIMARY KEY, original_url TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()


# Generate a random short ID (6 characters)
def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    short_id = ''.join(random.choice(chars) for _ in range(length))
    return short_id


# Home page
@app.route('/')
def index():
    return render_template('index.html')


# Create a shortened URL
@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']

    # Validate URL
    try:
        result = urlparse(original_url)
        if not all([result.scheme, result.netloc]):
            return "Invalid URL", 400
    except:
        return "Invalid URL", 400

    # Generate short ID
    short_id = generate_short_id()

    # Check for collisions and regenerate if needed
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    while True:
        existing = c.execute('SELECT id FROM links WHERE id = ?', (short_id,)).fetchone()
        if not existing:
            break
        short_id = generate_short_id()

    # Save to database
    c.execute('INSERT INTO links (id, original_url) VALUES (?, ?)',
              (short_id, original_url))
    conn.commit()
    conn.close()

    short_url = request.host_url + short_id
    return render_template('shortened.html', short_url=short_url)


# Redirect to original URL
@app.route('/<short_id>')
def redirect_to_url(short_id):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    result = c.execute('SELECT original_url FROM links WHERE id = ?',
                       (short_id,)).fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404


if __name__ == '__main__':
    if not os.path.exists('links.db'):
        init_db()
    app.run(debug=True)