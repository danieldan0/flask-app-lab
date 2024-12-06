from flask import Flask


def create_app(config_name="config"):
    app = Flask(__name__)
    app.config.from_object(config_name)

    with app.app_context():
        from . import views
        from .users import user_bp
        app.register_blueprint(user_bp)

        from .posts import post_bp
        app.register_blueprint(post_bp)
    
    return app