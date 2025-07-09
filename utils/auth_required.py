from functools import wraps
from flask import request, jsonify, redirect, url_for
from utils.jwt_helper import verify_token
from models.database import users_collection
from bson import ObjectId
from bson.errors import InvalidId

def auth_required(f):
    """JWT 토큰 인증이 필요한 라우트에 사용하는 데코레이터"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # 1. 헤더에서 토큰 찾기 (AJAX 요청용)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # "Bearer <token>" 형식
            except IndexError:
                pass
        
        # 2. 쿠키에서 토큰 찾기 (일반 페이지 요청용)
        if not token:
            token = request.cookies.get('access_token')
            print(f"[DEBUG] 쿠키에서 가져온 토큰: {token[:50] if token else None}...")  # 토큰 일부만 출력
        
        # 3. 토큰이 없는 경우
        if not token:
            print("[DEBUG] 토큰이 없음")
            if request.is_json:
                return jsonify({'message': '토큰이 필요합니다'}), 401
            else:
                return redirect(url_for('route.index'))  # 로그인 페이지로
        
        # 4. 토큰 검증
        user_id = verify_token(token)
        print(f"[DEBUG] 토큰 검증 결과 user_id: {user_id}")
        
        if not user_id:
            print("[DEBUG] 토큰 검증 실패")
            if request.is_json:
                return jsonify({'message': '유효하지 않은 토큰입니다'}), 401
            else:
                return redirect(url_for('route.index'))
        
        # 5. 사용자 존재 확인 (ObjectId로 변환)
        try:
            # 문자열을 ObjectId로 변환
            object_id = ObjectId(user_id)
            user = users_collection.find_one({'_id': object_id})
            print(f"[DEBUG] DB에서 찾은 사용자: {user}")
        except InvalidId:
            print(f"[DEBUG] 잘못된 ObjectId 형식: {user_id}")
            user = None
        except Exception as e:
            print(f"[DEBUG] DB 조회 오류: {e}")
            user = None
        
        if not user:
            print("[DEBUG] 사용자를 찾을 수 없음")
            if request.is_json:
                return jsonify({'message': '사용자를 찾을 수 없습니다'}), 401
            else:
                return redirect(url_for('route.index'))
        
        # 6. 인증 성공 - 사용자 정보를 함수에 전달
        print("[DEBUG] 인증 성공!")
        return f(current_user=user, *args, **kwargs)
    
    return decorated_function

def auth_optional(f):
    """선택적 인증 - 로그인하지 않아도 접근 가능하지만, 로그인했다면 사용자 정보 제공"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        current_user = None
        
        # 토큰 찾기
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                pass
        
        if not token:
            token = request.cookies.get('access_token')
        
        # 토큰이 있다면 검증
        if token:
            user_id = verify_token(token)
            if user_id:
                try:
                    object_id = ObjectId(user_id)
                    current_user = users_collection.find_one({'_id': object_id})
                except (InvalidId, Exception):
                    current_user = None
        
        return f(current_user=current_user, *args, **kwargs)
    
    return decorated_function