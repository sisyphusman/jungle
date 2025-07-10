from flask import Blueprint, request, jsonify, make_response, redirect, url_for, session
from models.user import (
    create_user, authenticate_user, find_user_by_id, update_user_slack_info, find_user_by_email
)
from utils.jwt_helper import generate_token
from utils.email_helper import send_verification_email, store_verification_code, verify_email_code, generate_verification_code
import requests
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """회원가입 1단계 - 이메일 인증 코드 발송"""
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

        # 이메일 중복 확인
        existing_user = find_user_by_email(email)
        if existing_user:
            return jsonify({
                'success': False,
                'message': '이미 가입된 이메일입니다'
            }), 400

        # 인증 코드 생성 및 발송
        verification_code = generate_verification_code()
        
        if send_verification_email(email, verification_code):
            if store_verification_code(email, verification_code):
                # 세션에 임시 회원가입 정보 저장
                session['temp_signup'] = {
                    'name': name,
                    'email': email,
                    'password': password,
                    'step': 'email_verification'
                }
                
                return jsonify({
                    'success': True,
                    'message': '인증 코드가 이메일로 발송되었습니다',
                    'step': 'email_verification'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': '인증 코드 저장에 실패했습니다'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': '이메일 발송에 실패했습니다'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'서버 오류: {str(e)}'
        }), 500

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """회원가입 2단계 - 이메일 인증 코드 확인"""
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        verification_code = data.get('verification_code')
        
        if not verification_code:
            return jsonify({
                'success': False,
                'message': '인증 코드를 입력해주세요'
            }), 400

        # 세션에서 임시 회원가입 정보 확인
        temp_signup = session.get('temp_signup')
        if not temp_signup or temp_signup.get('step') != 'email_verification':
            return jsonify({
                'success': False,
                'message': '회원가입 세션이 만료되었습니다. 다시 시도해주세요'
            }), 400

        # 인증 코드 검증
        if verify_email_code(temp_signup['email'], verification_code):
            # 인증 성공 - 실제 회원가입 진행
            from utils.slack_helper import get_slack_members
            
            slack_members = get_slack_members()
            slack_data = None
            
            if slack_members:
                for member in slack_members:
                    if member.get('email') == temp_signup['email']:
                        slack_data = member
                        break

            # 사용자 생성
            result = create_user(
                temp_signup['name'], 
                temp_signup['email'], 
                temp_signup['password'], 
                slack_data
            )

            if result['success']:
                # 세션 정리
                session.pop('temp_signup', None)
                
                return jsonify({
                    'success': True,
                    'message': '회원가입이 완료되었습니다!',
                    'has_slack': result.get('has_slack', False)
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': result.get('message')
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': '인증 코드가 올바르지 않거나 만료되었습니다'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'서버 오류: {str(e)}'
        }), 500

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """인증 코드 재발송"""
    try:
        temp_signup = session.get('temp_signup')
        if not temp_signup:
            return jsonify({
                'success': False,
                'message': '회원가입 세션이 없습니다'
            }), 400

        # 새 인증 코드 생성 및 발송
        verification_code = generate_verification_code()
        
        if send_verification_email(temp_signup['email'], verification_code):
            if store_verification_code(temp_signup['email'], verification_code):
                return jsonify({
                    'success': True,
                    'message': '인증 코드가 재발송되었습니다'
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': '인증 코드 저장에 실패했습니다'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': '이메일 발송에 실패했습니다'
            }), 500

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