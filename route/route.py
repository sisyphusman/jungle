from flask import Blueprint, render_template

route_bp = Blueprint('route', __name__)


@route_bp.route("/")
def index():
    return render_template("/login.html")


@route_bp.route("/signup")
def signup():
    return render_template("signup.html")


@route_bp.route("/home")
def home():
    return render_template("home.html")
