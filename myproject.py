from flask import Flask, request
from flask_session import Session
from config import Config
from modules.fails_handler.logging_bot import error_handler_flask
from blueprints import Blueprints
from database import DB

def create_app():
    def register_blueprints():
        for blueprint in Blueprints:
            app.register_blueprint(blueprint)
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.Flask.SECRET_KEY
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    register_blueprints()
    return app

app = create_app()

@app.route('/test_fail')
@error_handler_flask(request)
def test():
    x = 1 / 0
    return x
