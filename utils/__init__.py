from flask import Flask, Blueprint
from app.views import blue
from app.web_module import web



def create_app():
    app = Flask(__name__)
    # local test
    for_test_blue = Blueprint('for local test', __name__, static_folder='../pic/', static_url_path="")
    app.register_blueprint(blueprint=blue, url_prefix='/city360')
    app.register_blueprint(blueprint=for_test_blue)
    app.register_blueprint(web)
    return app
