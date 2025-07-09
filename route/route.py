from flask import Blueprint, render_template
from utils.auth_required import auth_required
from models.user import find_user_by_id



from models.card import get_cards

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
    cards = get_cards(1)
    return render_template("home.html", cards=cards)

# 임시로 인증 없이 접속 가능


@route_bp.route("/post")
def post():
    return render_template("post.html")

@route_bp.route("/mypage")
@auth_required
def mypage(current_user):
    from route.cal_user_stats import sum_all_users      
    result = sum_all_users(current_user.get("id"))

    return render_template("mypage.html", 
                            current_user=current_user,
                            user_posts=result.get("total_posts", 0),
                            total_likes=result.get("total_likes", 0),
                            active_days=result.get("total_active_days", 0))