from flask import Blueprint, request, jsonify, make_response, redirect, url_for, session
from models.user import (
    create_user, authenticate_user, 
    create_or_update_slack_user, find_user_by_slack_id
)
from utils.jwt_helper import generate_token
import requests
from config import Config

auth_bp = Blueprint('auth', __name__)

# =================== 기존 이메일/비밀번호 로그인 (그대로 유지) ===================

@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입 API (기존 방식)"""
    try:
        # JSON 또는 Form 데이터 받기
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        name = data.get('name') or data.get('text')  # signup.html에서 id="text"
        email = data.get('email')
        password = data.get('password')

        # 입력값 검증
        if not all([name, email, password]):
            return jsonify({
                'success': False,
                'message': '모든 필드를 입력해주세요'
            }), 400

        # 사용자 생성 (기존 함수 사용)
        result = create_user(name, email, password)

        if result['success']:
            print("사용자 생성 성공: ", end="")
            print(result)
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'서버 오류: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """로그인 API (기존 방식)"""
    try:
        # JSON 또는 Form 데이터 받기
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        email = data.get('email')
        password = data.get('password')

        # 입력값 검증
        if not all([email, password]):
            return jsonify({
                'success': False,
                'message': '이메일과 비밀번호를 입력해주세요'
            }), 400

        # 사용자 인증 (기존 함수 사용)
        auth_result = authenticate_user(email, password)

        if auth_result['success']:
            # JWT 토큰 생성
            user_id = auth_result['user']['id']
            token = generate_token(user_id)

            # 응답 생성
            response_data = {
                'success': True,
                'message': '로그인 성공',
                'user': auth_result['user'],
            }

            # 쿠키에 토큰 저장하여 응답
            response = make_response(jsonify(response_data))
            response.set_cookie(
                'access_token',
                token,
                max_age=60*60*2,  # 2시간
                httponly=True,    # XSS 방지
                secure=False,     # 개발환경에서는 False
                samesite='Lax'
            )

            return response, 200
        else:
            return jsonify(auth_result), 401

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'서버 오류: {str(e)}'
        }), 500
