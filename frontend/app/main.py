from flask import Flask, session
import random

# Config
from .config import ConfigFlask, ConfigLog


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = ConfigFlask.SECRET

    @app.before_request
    def set_session():
        if "user_id" not in session:
            session.permanent = True
            session["user_id"] = random.getrandbits(32)

    # Pages
    from .errors.handler import errors
    from .pages.base.routes import base
    from .pages.item.routes import item
    from .pages.shop.routes import shop
    from .pages.cart.routes import cart
    app.register_blueprint(errors)
    app.register_blueprint(base)
    app.register_blueprint(item)
    app.register_blueprint(shop)
    app.register_blueprint(cart)

    return app
