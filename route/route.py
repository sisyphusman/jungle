from flask import Blueprint, render_template
# from utils.auth_required import auth_required  # 임시 주석

route_bp = Blueprint('route', __name__)

# 인증 불필요 - 로그인 페이지
@route_bp.route("/")
def index():
    return render_template("login.html")

# 인증 불필요 - 회원가입 페이지  
@route_bp.route("/signup")
def signup():
    return render_template("signup.html")

# 임시로 인증 없이 접속 가능
@route_bp.route("/home")
def home():
    return render_template("home.html")

# 임시로 인증 없이 접속 가능
@route_bp.route("/post")
def post():
    return render_template("post.html")