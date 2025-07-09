import requests
import urllib.parse
from config import Config

def get_slack_oauth_url(state):
    """Slack OAuth 인증 URL 생성"""
    try:
        base_url = "https://slack.com/oauth/v2/authorize"
        
        params = {
            'client_id': Config.SLACK_CLIENT_ID,
            'scope': 'users:read,users:read.email',
            'redirect_uri': f"{Config.BASE_URL}/auth/slack/callback",
            'state': state,
            'user_scope': 'users:read,users:read.email'
        }
        
        # Team ID가 설정되어 있으면 추가 (워크스페이스 직접 지정)
        if Config.SLACK_TEAM_ID:
            params['team'] = Config.SLACK_TEAM_ID
        
        # URL 인코딩
        query_string = urllib.parse.urlencode(params)
        oauth_url = f"{base_url}?{query_string}"
        
        print(f"🔗 생성된 OAuth URL: {oauth_url}")  # 디버깅용
        
        return oauth_url
        
    except Exception as e:
        print(f"Slack OAuth URL 생성 실패: {e}")
        return None

def exchange_code_for_token(code):
    """인증 코드를 액세스 토큰으로 교환"""
    try:
        url = "https://slack.com/api/oauth.v2.access"
        
        data = {
            'client_id': Config.SLACK_CLIENT_ID,
            'client_secret': Config.SLACK_CLIENT_SECRET,
            'code': code,
            'redirect_uri': f"{Config.BASE_URL}/auth/slack/callback"
        }
        
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get('ok'):
            return {
                'success': True,
                'access_token': result['authed_user']['access_token'],
                'team_id': result['team']['id'],
                'user_id': result['authed_user']['id']
            }
        else:
            print(f"토큰 교환 실패: {result.get('error')}")
            return {
                'success': False, 
                'error': result.get('error', 'unknown_error')
            }
            
    except Exception as e:
        print(f"토큰 교환 중 오류: {e}")
        return {'success': False, 'error': str(e)}

def get_slack_user_info(access_token):
    """Slack 사용자 정보 조회"""
    try:
        url = "https://slack.com/api/users.info"
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # 먼저 현재 사용자의 ID를 가져옴
        auth_response = requests.get(
            "https://slack.com/api/auth.test",
            headers=headers
        )
        auth_result = auth_response.json()
        
        if not auth_result.get('ok'):
            return {
                'success': False,
                'error': auth_result.get('error', 'auth_test_failed')
            }
            
        user_id = auth_result['user_id']
        team_id = auth_result['team_id']
        
        # 사용자 상세 정보 조회
        params = {'user': user_id}
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        if result.get('ok'):
            user_data = result['user']
            # team 정보 추가
            user_data['team'] = {'id': team_id}
            
            return {
                'success': True,
                'user_data': user_data
            }
        else:
            print(f"사용자 정보 조회 실패: {result.get('error')}")
            return {
                'success': False,
                'error': result.get('error', 'user_info_failed')
            }
            
    except Exception as e:
        print(f"사용자 정보 조회 중 오류: {e}")
        return {'success': False, 'error': str(e)}