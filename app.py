from flask import Flask, render_template
import os
from config import Config


def create_app(config_class=Config):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    from services.link_shortener.utils import init_db
    with app.app_context():
        init_db()

    # Register blueprints
    from services.link_shortener.routes import bp as links_bp
    app.register_blueprint(links_bp)

    # Root route for the main page
    @app.route('/')
    def index():
        return render_template('base.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)