from flask import Blueprint, request, jsonify, make_response, redirect, url_for, session
from models.user import (
    create_user, authenticate_user, find_user_by_id, update_user_slack_info
)
from utils.jwt_helper import generate_token
import requests
from config import Config

auth_bp = Blueprint('auth', __name__)

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

        print(f"\n=== 회원가입 디버깅 시작 ===")
        print(f"요청자: {name}")
        print(f"회원가입 요청 이메일: '{email}'")

        # 1. Slack 멤버 최신화
        from utils.slack_helper import get_slack_members
        slack_members = get_slack_members()
        
        # 🔍 여기에 토큰 디버깅 코드 추가
        print(f"=== 토큰 디버깅 ===")
        print(f"Flask 앱 토큰: {Config.SLACK_BOT_TOKEN[:20]}...")
        
        
        print(f"Slack 멤버 수: {len(slack_members) if slack_members else 0}")
        
        if slack_members:
            print("\n현재 Slack 워크스페이스 멤버 목록:")
            for i, member in enumerate(slack_members, 1):
                print(f"  [{i}] {member.get('name', 'Unknown')} - '{member.get('email', 'None')}'")
        else:
            print("❌ Slack 멤버 정보를 가져올 수 없음")

        # 2. 이메일로 Slack 멤버 찾기
        slack_data = None
        print(f"\n=== 이메일 매칭 시도 ===")
        
        if slack_members:
            for i, member in enumerate(slack_members, 1):
                slack_email = member.get('email', '')
                print(f"[{i}] 비교: '{slack_email}' == '{email}' ? {slack_email == email}")
                
                if slack_email == email:
                    slack_data = member
                    print(f"✅ 매칭 성공! Slack 사용자: {member.get('name')} (ID: {member.get('slack_user_id')})")
                    break
            
            if not slack_data:
                print(f"❌ 매칭 실패: '{email}'이 Slack 멤버 목록에 없음")
        else:
            print("Slack 멤버 정보가 없어서 매칭 불가")

        # 3. 사용자 생성 (Slack 정보 포함 또는 제외)
        print(f"\n=== 사용자 생성 ===")
        result = create_user(name, email, password, slack_data)

        if result['success']:
            print(f"✅ 사용자 생성 성공: {name} ({email})")
            if result.get('has_slack'):
                print(f"   - Slack 정보 연동됨: {slack_data['slack_user_id']}")
                print(f"   - Slack 이름: {slack_data.get('name')}")
                print(f"   - 아바타: {slack_data.get('avatar_url')}")
            else:
                print(f"   - 일반 회원가입 (Slack 정보 없음)")
            
            print(f"=== 회원가입 디버깅 완료 ===\n")
            return jsonify(result), 201
        else:
            print(f"❌ 사용자 생성 실패: {result.get('message')}")
            print(f"=== 회원가입 디버깅 완료 ===\n")
            return jsonify(result), 400

    except Exception as e:
        print(f"❌ 서버 오류: {str(e)}")
        print(f"=== 회원가입 디버깅 완료 ===\n")
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