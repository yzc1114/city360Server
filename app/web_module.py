from flask import Blueprint

web = Blueprint('city_web_blue', __name__, url_prefix='/city360_web', static_folder='../city360', static_url_path="")

@web.route("/")
def hello():
    return web.send_static_file('index.html')