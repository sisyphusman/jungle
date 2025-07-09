from flask import Blueprint, request, jsonify, make_response, redirect, url_for, session
from models.user import (
    create_user, authenticate_user, find_user_by_id, update_user_slack_info
)
from utils.jwt_helper import generate_token
import requests
from config import Config

auth_bp = Blueprint('auth', __name__)

# =================== 기존 이메일/비밀번호 로그인 (그대로 유지) ===================

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     """회원가입 API (기존 방식)"""
#     try:
#         # JSON 또는 Form 데이터 받기
#         if request.is_json:
#             data = request.get_json()
#         else:
#             data = request.form

#         name = data.get('name') or data.get('text')  # signup.html에서 id="text"
#         email = data.get('email')
#         password = data.get('password')

#         # 입력값 검증
#         if not all([name, email, password]):
#             return jsonify({
#                 'success': False,
#                 'message': '모든 필드를 입력해주세요'
#             }), 400

#         # 사용자 생성 (기존 함수 사용)
#         result = create_user(name, email, password)

#         if result['success']:
#             print("사용자 생성 성공: ", end="")
#             print(result)
#             return jsonify(result), 201
#         else:
#             return jsonify(result), 400

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'서버 오류: {str(e)}'
#         }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입 API (Slack 자동 매칭)"""
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

        # 1. Slack 멤버 최신화
        from utils.slack_helper import get_slack_members
        slack_members = get_slack_members()
        
        # 2. 이메일로 Slack 멤버 찾기
        slack_data = None
        if slack_members:
            for member in slack_members:
                if member['email'] == email:
                    slack_data = member
                    break

        # 3. 사용자 생성 (Slack 정보 포함 또는 제외)
        result = create_user(name, email, password, slack_data)

        if result['success']:
            print(f"사용자 생성 성공: {name} ({email})")
            if result.get('has_slack'):
                print(f"  - Slack 정보 연동됨: {slack_data['slack_user_id']}")
            else:
                print(f"  - 일반 회원가입 (Slack 정보 없음)")
            
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

# =================== 새로 추가: Slack 동기화 엔드포인트 ===================

@auth_bp.route('/sync-slack', methods=['POST'])
def sync_slack():
    """회원가입 후 Slack 정보 동기화"""
    try:
        from utils.slack_helper import get_slack_members
        
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        email = data.get('email')
        
        if not email:
            return jsonify({
                'success': False,
                'message': '이메일이 필요합니다'
            }), 400
        
        # Slack 멤버 정보 가져오기
        slack_members = get_slack_members()
        if not slack_members:
            return jsonify({
                'success': False,
                'message': 'Slack 멤버 정보를 가져올 수 없습니다'
            }), 500
        
        # 이메일로 매칭
        matching_member = None
        for member in slack_members:
            if member['email'] == email:
                matching_member = member
                break
        
        if not matching_member:
            return jsonify({
                'success': False,
                'message': '해당 이메일의 Slack 멤버를 찾을 수 없습니다'
            })
        
        # 사용자 Slack 정보 업데이트
        slack_data = {
            'slack_user_id': matching_member['slack_user_id'],
            'slack_team_id': matching_member['slack_team_id'],
            'avatar_url': matching_member['avatar_url'],
            'real_name': matching_member['real_name'],
            'display_name': matching_member['display_name']
        }
        
        result = update_user_slack_info(email, slack_data)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Slack 정보 동기화 완료'
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'서버 오류: {str(e)}'
        }), 500