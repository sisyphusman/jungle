from flask import Blueprint, render_template
from utils.auth_required import auth_required




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
    # 임시로 빈 데이터로 렌더링
    return render_template("mypage.html", 
                         current_user=current_user,
                         user_posts=[],
                         total_likes=0,
                         active_days=0)

@route_bp.route("/debug-routes")
def debug_routes():
    """등록된 모든 라우트 확인"""
    from flask import current_app
    
    routes = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
        routes.append(f"{rule.rule} [{methods}] -> {rule.endpoint}")
    
    routes_html = "<br>".join(sorted(routes))
    
    return f"""
    <h1>🛠 등록된 라우트 목록</h1>
    <p>총 {len(routes)}개의 라우트가 등록되어 있습니다:</p>
    <div style="font-family: monospace; background: #f5f5f5; padding: 10px;">
        {routes_html}
    </div>
    """