from functools import wraps
from flask import request, jsonify, redirect, url_for, session
from utils.jwt_helper import verify_token
from models.user import find_user_by_id, find_user_by_slack_id

def auth_required(f):
    """JWT 토큰 또는 Slack 세션 인증이 필요한 라우트에 사용하는 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = None
        
        # 방법 1: Slack 세션 확인 (우선순위)
        if session.get('login_type') == 'slack':
            slack_user_id = session.get('user_id')
            slack_team_id = session.get('team_id')
            
            if slack_user_id and slack_team_id:
                # 기존 함수 사용
                slack_user = find_user_by_slack_id(slack_user_id, slack_team_id)
                if slack_user:
                    current_user = slack_user
                    current_user['login_type'] = 'slack'
                    print(f"[DEBUG] Slack 세션 인증 성공: {slack_user['name']}")
        
        # 방법 2: JWT 토큰 확인 (기존 방식)
        if not current_user:
            token = None
            
            # 헤더에서 토큰 찾기 (AJAX 요청용)
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]  # "Bearer <token>" 형식
                except IndexError:
                    pass
            
            # 쿠키에서 토큰 찾기 (일반 페이지 요청용)
            if not token:
                token = request.cookies.get('access_token')
            
            if token:
                # JWT 토큰 검증
                user_id = verify_token(token)
                print(f"[DEBUG] JWT 토큰 검증 결과 user_id: {user_id}")
                
                if user_id:
                    # 기존 함수 사용
                    user = find_user_by_id(user_id)
                    if user:
                        current_user = user
                        current_user['login_type'] = 'email'
                        print(f"[DEBUG] JWT 인증 성공: {current_user['name']}")
        
        # 인증 실패 처리
        if not current_user:
            print("[DEBUG] 인증 실패 - 토큰/세션 없음")
            if request.is_json:
                return jsonify({'message': '로그인이 필요합니다'}), 401
            else:
                return redirect(url_for('route.index'))  # 로그인 페이지로
        
        # 인증 성공 - 사용자 정보를 함수에 전달
        print(f"[DEBUG] 인증 성공! 사용자: {current_user['name']} ({current_user['login_type']})")
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated_function

def auth_optional(f):
    """선택적 인증 - 로그인하지 않아도 접근 가능하지만, 로그인했다면 사용자 정보 제공"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = None
        
        # 방법 1: Slack 세션 확인
        if session.get('login_type') == 'slack':
            slack_user_id = session.get('user_id')
            slack_team_id = session.get('team_id')
            
            if slack_user_id and slack_team_id:
                slack_user = find_user_by_slack_id(slack_user_id, slack_team_id)
                if slack_user:
                    current_user = slack_user
                    current_user['login_type'] = 'slack'
        
        # 방법 2: JWT 토큰 확인
        if not current_user:
            token = None
            
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(" ")[1]
                except IndexError:
                    pass
            
            if not token:
                token = request.cookies.get('access_token')
            
            if token:
                user_id = verify_token(token)
                if user_id:
                    user = find_user_by_id(user_id)
                    if user:
                        current_user = user
                        current_user['login_type'] = 'email'
        
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated_function

def get_current_user():
    """현재 로그인한 사용자 정보 반환 (유틸리티 함수)"""
    # Slack 세션 확인
    if session.get('login_type') == 'slack':
        slack_user_id = session.get('user_id')
        slack_team_id = session.get('team_id')
        
        if slack_user_id and slack_team_id:
            user = find_user_by_slack_id(slack_user_id, slack_team_id)
            if user:
                user['login_type'] = 'slack'
                return user
    
    # JWT 토큰 확인
    token = request.cookies.get('access_token')
    if token:
        user_id = verify_token(token)
        if user_id:
            user = find_user_by_id(user_id)
            if user:
                user['login_type'] = 'email'
                return user
    
    return None