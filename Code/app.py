from flask import Flask, session, abort, render_template
from config import Config
from flask_wtf.csrf import CSRFProtect
from auth import bp as auth_bp
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute", "100 per hour"],
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CSRFProtect(app)
    limiter.init_app(app)

    app.register_blueprint(auth_bp)

    @app.route('/dashboard')
    def dashboard():
        if not session.get('user_id'):
            return render_template("unauthorized.html"), 401
        return render_template("dashboard.html")

    return app