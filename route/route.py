from flask import Blueprint, render_template
from utils.auth_required import auth_required

route_bp = Blueprint('route', __name__)

# 인증 불필요 - 로그인 페이지
@route_bp.route("/")
def index():
    return render_template("/login.html")

# 인증 불필요 - 회원가입 페이지  
@route_bp.route("/signup")
def signup():
    return render_template("signup.html")

# 인증 필요 - 메인 페이지
@route_bp.route("/home")
@auth_required
def home(current_user):
    return render_template("home.html", user=current_user)

# 인증 필요 - TIL 작성 페이지
@route_bp.route("/post")
@auth_required
def post(current_user):
    return render_template("post.html", user=current_user)