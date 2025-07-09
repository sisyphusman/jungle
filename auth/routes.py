# from flask import Blueprint, request, jsonify, make_response, redirect, url_for, session
# from models.user import create_user, authenticate_user, create_or_update_slack_user, find_user_by_slack_id
# from utils.jwt_helper import generate_token
# from utils.slack_helper import get_slack_oauth_url, exchange_code_for_token, get_slack_user_info
# import secrets

# auth_bp = Blueprint('auth', __name__)

# # === 기존 이메일/비밀번호 로그인 ===
# @auth_bp.route('/register', methods=['POST'])
# def register():
#     """회원가입 API"""
#     try:
#         if request.is_json:
#             data = request.get_json()
#         else:
#             data = request.form

#         name = data.get('name') or data.get('text')
#         email = data.get('email')
#         password = data.get('password')

#         if not all([name, email, password]):
#             return jsonify({
#                 'success': False,
#                 'message': '모든 필드를 입력해주세요'
#             }), 400

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

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     """이메일/비밀번호 로그인 API"""
#     try:
#         if request.is_json:
#             data = request.get_json()
#         else:
#             data = request.form

#         email = data.get('email')
#         password = data.get('password')

#         if not all([email, password]):
#             return jsonify({
#                 'success': False,
#                 'message': '이메일과 비밀번호를 입력해주세요'
#             }), 400

#         auth_result = authenticate_user(email, password)

#         if auth_result['success']:
#             user_id = auth_result['user']['id']
#             token = generate_token(user_id)

#             response_data = {
#                 'success': True,
#                 'message': '로그인 성공',
#                 'user': auth_result['user'],
#             }

#             response = make_response(jsonify(response_data))
#             response.set_cookie(
#                 'access_token',
#                 token,
#                 max_age=60*60*2,
#                 httponly=True,
#                 secure=False,
#                 samesite='Lax'
#             )

#             return response, 200
#         else:
#             return jsonify(auth_result), 401

#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'서버 오류: {str(e)}'
#         }), 500

# # === Slack OAuth2 구현 ===
# @auth_bp.route('/slack/login', methods=['GET'])
# def slack_login():
#     """Slack OAuth 로그인 시작"""
#     try:
#         state = secrets.token_urlsafe(32)
#         session['oauth_state'] = state
        
#         oauth_url = get_slack_oauth_url(state)
        
#         if not oauth_url:
#             return jsonify({
#                 'success': False, 
#                 'message': 'Slack OAuth 설정이 올바르지 않습니다'
#             }), 500
            
#         return redirect(oauth_url)
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'Slack 로그인 시작 실패: {str(e)}'
#         }), 500

# @auth_bp.route('/slack/callback', methods=['GET'])
# def slack_callback():
#     """Slack OAuth 콜백 처리"""
#     try:
#         error = request.args.get('error')
#         if error:
#             return redirect(url_for('route.index', error='slack_login_denied'))
        
#         code = request.args.get('code')
#         state = request.args.get('state')
        
#         if not code:
#             return redirect(url_for('route.index', error='no_auth_code'))
            
#         if not state or state != session.get('oauth_state'):
#             return redirect(url_for('route.index', error='invalid_state'))
            
#         session.pop('oauth_state', None)
        
#         token_response = exchange_code_for_token(code)
#         if not token_response['success']:
#             return redirect(url_for('route.index', error='token_exchange_failed'))
            
#         access_token = token_response['access_token']
        
#         user_info_response = get_slack_user_info(access_token)
#         if not user_info_response['success']:
#             return redirect(url_for('route.index', error='user_info_failed'))
            
#         slack_user_data = user_info_response['user_data']
        
#         user_result = create_or_update_slack_user(slack_user_data)
#         if not user_result['success']:
#             return redirect(url_for('route.index', error='user_creation_failed'))
        
#         user_id = user_result['user_id']
#         jwt_token = generate_token(user_id)
        
#         response = make_response(redirect(url_for('route.home')))
#         response.set_cookie(
#             'access_token',
#             jwt_token,
#             max_age=60*60*2,
#             httponly=True,
#             secure=False,
#             samesite='Lax'
#         )
        
#         session['user_id'] = user_id
#         session['slack_user_id'] = slack_user_data['id']
#         session['slack_team_id'] = slack_user_data['team']['id']
        
#         return response
        
#     except Exception as e:
#         print(f"Slack callback 오류: {e}")
#         return redirect(url_for('route.index', error='callback_error'))

# # === 공통 로그아웃 (기존 + Slack 통합) ===
# @auth_bp.route('/logout', methods=['POST'])
# def logout():
#     """통합 로그아웃 (이메일/비밀번호 + Slack)"""
#     try:
#         response = make_response(jsonify({
#             'success': True,
#             'message': '로그아웃 성공'
#         }))
        
#         # 쿠키에서 토큰 삭제
#         response.set_cookie('access_token', '', expires=0)
        
#         # 세션 정리 (Slack 정보 포함)
#         session.clear()
        
#         return response, 200
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'서버 오류: {str(e)}'
#         }), 500

# @auth_bp.route('/profile', methods=['GET'])
# def get_profile():
#     """현재 로그인된 사용자 프로필 조회"""
#     try:
#         user_id = session.get('user_id')
#         if not user_id:
#             return jsonify({'success': False, 'message': '로그인이 필요합니다'}), 401
            
#         from models.user import find_user_by_id
#         user = find_user_by_id(user_id)
        
#         if not user:
#             return jsonify({'success': False, 'message': '사용자를 찾을 수 없습니다'}), 404
            
#         return jsonify({
#             'success': True,
#             'user': user
#         })
        
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'message': f'프로필 조회 실패: {str(e)}'
#         }), 500

# auth/routes.py - 기존 이메일/비밀번호 + Slack OAuth 하이브리드

# auth/routes.py - 기존 user.py 함수들을 활용한 버전

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

# =================== Slack OAuth 로그인 (수정된 버전) ===================

@auth_bp.route('/slack')
def slack_oauth():
    """Slack OAuth 시작"""
    
    # 가입용인지 로그인용인지 구분
    action = request.args.get('action', 'login')
    
    # 상태값 생성 (나중에 검증용)
    state = f"action_{action}"
    session['oauth_state'] = state
    
    # OAuth URL 생성
    oauth_url = (
        f"https://slack.com/oauth/v2/authorize?"
        f"client_id={Config.SLACK_CLIENT_ID}&"
        f"scope=openid,profile,email&" 
        f"redirect_uri={Config.BASE_URL}/auth/slack/callback&"
        f"state={state}"
    )
    
    # 워크스페이스 고정 (선택사항)
    if Config.SLACK_TEAM_ID:
        oauth_url += f"&team={Config.SLACK_TEAM_ID}"
    
    print(f"[DEBUG] OAuth URL: {oauth_url}")  # 디버깅용

    return redirect(oauth_url)

# @auth_bp.route('/slack/callback')
# def slack_callback():
#     """Slack OAuth 콜백 처리"""
#     code = request.args.get('code')
#     state = request.args.get('state')
#     error = request.args.get('error')
    
#     # 오류 처리
#     if error:
#         return redirect(url_for('route.index') + '?error=oauth_denied')
    
#     if not code:
#         return redirect(url_for('route.index') + '?error=missing_code')
    
#     # 상태값 검증
#     if state != session.get('oauth_state'):
#         return redirect(url_for('route.index') + '?error=invalid_state')
    
#     try:
#         # 1단계: 토큰 교환
#         # token_response = requests.post('https://slack.com/api/oauth.v2.access', {
#         #     'client_id': Config.SLACK_CLIENT_ID,
#         #     'client_secret': Config.SLACK_CLIENT_SECRET,
#         #     'code': code,
#         #     'redirect_uri': f'{Config.BASE_URL}/auth/slack/callback'
#         # })
#         token_response = requests.post(
#     'https://slack.com/api/oauth.v2.access', 
#     data=token_data,
#     verify=False  # 개발 환경에서만 사용
# )
        
#         token_data = token_response.json()
        
#         if not token_data.get('ok'):
#             print(f"토큰 교환 실패: {token_data}")
#             return redirect(url_for('route.index') + '?error=token_exchange_failed')
        
#         # 2단계: 워크스페이스 검증
#         team_id = token_data.get('team', {}).get('id')
#         if Config.SLACK_TEAM_ID and team_id != Config.SLACK_TEAM_ID:
#             return redirect(url_for('route.index') + '?error=wrong_workspace')
        
#         # 3단계: 사용자 정보 가져오기 (users.info API 사용)
#         user_token = token_data.get('authed_user', {}).get('access_token')
#         user_id = token_data.get('authed_user', {}).get('id')
        
#         # Bot 토큰으로 더 많은 사용자 정보 가져오기
#         user_info_response = requests.get(
#             'https://slack.com/api/users.info',
#             headers={'Authorization': f'Bearer {Config.SLACK_BOT_TOKEN}'},
#             params={'user': user_id}
#         )
        
#         user_info_data = user_info_response.json()
        
#         if not user_info_data.get('ok'):
#             # 대안: Identity API 사용
#             identity_response = requests.get(
#                 'https://slack.com/api/users.identity',
#                 headers={'Authorization': f'Bearer {user_token}'}
#             )
#             identity_data = identity_response.json()
            
#             if not identity_data.get('ok'):
#                 return redirect(url_for('route.index') + '?error=user_info_failed')
            
#             # Identity API 응답을 users.info 형태로 변환
#             slack_user_data = {
#                 'id': identity_data['user']['id'],
#                 'name': identity_data['user']['name'],
#                 'team': {'id': identity_data['team']['id']},
#                 'profile': {
#                     'real_name': identity_data['user']['name'],
#                     'display_name': identity_data['user']['name'],
#                     'email': identity_data['user']['email'],
#                     'image_192': identity_data['user']['image_192']
#                 }
#             }
#         else:
#             # users.info API 응답 사용
#             slack_user_data = user_info_data['user']
        
#         # 디버깅용 출력 (선택사항)
#         print("=== Slack 사용자 정보 ===")
#         print(f"User ID: {slack_user_data.get('id')}")
#         print(f"Name: {slack_user_data.get('name')}")
#         print(f"Team ID: {slack_user_data.get('team', {}).get('id')}")
#         print(f"Profile: {slack_user_data.get('profile', {})}")
        
#         # 4단계: 기존 create_or_update_slack_user 함수 사용
#         result = create_or_update_slack_user(slack_user_data)
        
#         if result['success']:
#             # 5단계: 세션 생성
#             session.clear()
#             session['user_id'] = result['user']['slack_user_id']
#             session['team_id'] = result['user']['slack_team_id']
#             session['nickname'] = result['user']['name']
#             session['avatar_url'] = result['user']['avatar_url']
#             session['login_type'] = 'slack'
#             session['db_user_id'] = result['user']['id']  # MongoDB _id
            
#             print(f"Slack 로그인 성공: {result['user']['name']}")
            
#             # 🎯 성공하면 무조건 /home으로!
#             return redirect(url_for('route.home'))
#         else:
#             print(f"사용자 저장 실패: {result['message']}")
#             return redirect(url_for('route.index') + '?error=user_save_failed')
            
#     except Exception as e:
#         print(f"Slack OAuth 콜백 오류: {e}")
#         return redirect(url_for('route.index') + '?error=callback_error')

# =================== 공통 로그아웃 ===================

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """로그아웃 API (기존 + Slack 통합)"""
    try:
        response = make_response(jsonify({
            'success': True,
            'message': '로그아웃 성공'
        }))

        # 쿠키에서 토큰 삭제 (기존 방식)
        response.set_cookie('access_token', '', expires=0)
        
        # 세션 클리어 (Slack 방식)
        session.clear()

        return response, 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'서버 오류: {str(e)}'
        }), 500
    

@auth_bp.route('/debug')
def debug_config():
    """설정 디버깅용"""
    return f"""
    <h1>설정 디버깅</h1>
    <p>BASE_URL: {Config.BASE_URL}</p>
    <p>SLACK_CLIENT_ID: {Config.SLACK_CLIENT_ID}</p>
    <p>SLACK_TEAM_ID: {Config.SLACK_TEAM_ID}</p>
    <p>예상 콜백 URL: {Config.BASE_URL}/auth/slack/callback</p>
    <p>OAuth URL: <a href="/auth/slack">테스트 링크</a></p>
    """



@auth_bp.route('/test-callback')
def test_callback():
    """콜백 라우트 테스트"""
    return """
    <h1>콜백 테스트 성공!</h1>
    <p>이 페이지가 보인다면 콜백 라우트가 올바르게 등록되었습니다.</p>
    <p><a href="/">홈으로 돌아가기</a></p>
    """

@auth_bp.route('/debug-info')
def debug_info():
    """현재 설정 정보 표시"""
    return f"""
    <h1>디버깅 정보</h1>
    <ul>
        <li>BASE_URL: {Config.BASE_URL}</li>
        <li>SLACK_CLIENT_ID: {Config.SLACK_CLIENT_ID}</li>
        <li>SLACK_TEAM_ID: {Config.SLACK_TEAM_ID}</li>
        <li>예상 콜백 URL: {Config.BASE_URL}/auth/slack/callback</li>
    </ul>
    <p><a href="/auth/slack">Slack 로그인 테스트</a></p>
    <p><a href="/auth/test-callback">콜백 라우트 테스트</a></p>
    """

@auth_bp.route('/slack/callback', methods=['GET', 'POST'])
def slack_callback():
    """Slack OAuth 콜백 처리 - 향상된 디버깅 버전"""
    print("="*50)
    print("🔥 콜백 라우트 진입!")
    print("="*50)
    
    # 모든 요청 정보 로깅
    print(f"요청 메소드: {request.method}")
    print(f"요청 URL: {request.url}")
    print(f"요청 경로: {request.path}")
    print(f"쿼리 파라미터: {dict(request.args)}")
    print(f"헤더: {dict(request.headers)}")
    
    # 쿼리 파라미터 추출
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    print(f"받은 파라미터:")
    print(f"  - code: {code[:20] if code else None}...")
    print(f"  - state: {state}")
    print(f"  - error: {error}")
    
    # 세션 정보 확인
    print(f"세션 상태: {dict(session)}")
    print(f"저장된 oauth_state: {session.get('oauth_state')}")
    
    # 에러 처리
    if error:
        print(f"❌ OAuth 에러: {error}")
        return f"""
        <h1>OAuth 에러 발생</h1>
        <p>에러: {error}</p>
        <p><a href="/">홈으로 돌아가기</a></p>
        """
    
    if not code:
        print("❌ 인증 코드 없음")
        return f"""
        <h1>인증 코드 없음</h1>
        <p>Slack에서 인증 코드를 받지 못했습니다.</p>
        <p><a href="/">홈으로 돌아가기</a></p>
        """
    
    # 상태값 검증
    expected_state = session.get('oauth_state')
    if state != expected_state:
        print(f"❌ 상태값 불일치: 받은값={state}, 예상값={expected_state}")
        return f"""
        <h1>상태값 불일치</h1>
        <p>보안 검증에 실패했습니다.</p>
        <p>받은 상태값: {state}</p>
        <p>예상 상태값: {expected_state}</p>
        <p><a href="/">홈으로 돌아가기</a></p>
        """
    
    print("✅ 기본 검증 통과!")
    
    try:
        # 토큰 교환 시도
        print("🔄 토큰 교환 시도...")
        
        token_data = {
            'client_id': Config.SLACK_CLIENT_ID,
            'client_secret': Config.SLACK_CLIENT_SECRET,
            'code': code,
            'redirect_uri': f'{Config.BASE_URL}/auth/slack/callback'
        }
        
        print(f"토큰 교환 데이터: {token_data}")
        
        response = requests.post(
            'https://slack.com/api/oauth.v2.access',
            data=token_data,
            verify=False
        )
        
        result = response.json()
        print(f"토큰 교환 응답: {result}")
        
        if result.get('ok'):
            print("✅ 토큰 교환 성공!")
            
            # 간단한 성공 페이지 반환 (DB 저장은 나중에)
            return f"""
            <h1>🎉 로그인 성공!</h1>
            <p>토큰 교환이 성공했습니다.</p>
            <p>사용자 ID: {result.get('authed_user', {}).get('id')}</p>
            <p>팀 ID: {result.get('team', {}).get('id')}</p>
            <p><a href="/home">홈으로 이동</a></p>
            """
        else:
            print(f"❌ 토큰 교환 실패: {result}")
            return f"""
            <h1>토큰 교환 실패</h1>
            <p>에러: {result.get('error', 'unknown')}</p>
            <p>상세: {result}</p>
            <p><a href="/">홈으로 돌아가기</a></p>
            """
            
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        import traceback
        traceback.print_exc()
        
        return f"""
        <h1>예외 발생</h1>
        <p>오류: {str(e)}</p>
        <p><a href="/">홈으로 돌아가기</a></p>
        """
    
