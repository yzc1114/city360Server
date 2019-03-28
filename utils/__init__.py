from flask import Flask
from app.views import blue
from app.web_module import web



def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint=blue, url_prefix='/city360')
    app.register_blueprint(web)
    return app
