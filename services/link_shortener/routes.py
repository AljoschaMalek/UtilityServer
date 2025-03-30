from flask import Blueprint, request, redirect, render_template, g, current_app
from urllib.parse import urlparse
from .utils import get_db, generate_short_id, close_db

# Create a blueprint for the link shortener
bp = Blueprint('links', __name__, url_prefix='/links')

# Make sure we close the db connection when the request is done
bp.teardown_request(close_db)


@bp.route('/')
def index():
    return render_template('link_shortener/index.html')


@bp.route('/shorten', methods=['POST'])
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
    db = get_db()
    while True:
        existing = db.execute('SELECT id FROM links WHERE id = ?', (short_id,)).fetchone()
        if not existing:
            break
        short_id = generate_short_id()

    # Save to database
    db.execute('INSERT INTO links (id, original_url) VALUES (?, ?)',
               (short_id, original_url))
    db.commit()

    short_url = request.host_url + 'links/' + short_id
    return render_template('link_shortener/shortened.html', short_url=short_url)


@bp.route('/<short_id>')
def redirect_to_url(short_id):
    db = get_db()
    result = db.execute('SELECT original_url FROM links WHERE id = ?',
                        (short_id,)).fetchone()

    if result:
        return redirect(result['original_url'])
    else:
        return "URL not found", 404