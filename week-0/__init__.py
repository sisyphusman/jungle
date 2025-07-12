from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 현재 실제로 사용하는 Blueprint만 등록
    from route.route import route_bp
    app.register_blueprint(route_bp)

    from auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from models.card import card_bp
    app.register_blueprint(card_bp, url_prefix='/models')

    return app
