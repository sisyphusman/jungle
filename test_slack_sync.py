#!/usr/bin/env python3
"""
Slack 멤버 정보 동기화 테스트 스크립트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.slack_helper import get_slack_members, test_slack_connection
from config import Config

def main():
    print("=== Slack 멤버 정보 동기화 테스트 ===\n")
    
    # 1. 환경변수 확인
    print("1. 환경변수 확인:")
    if Config.SLACK_BOT_TOKEN:
        print(f"   ✅ SLACK_BOT_TOKEN: {Config.SLACK_BOT_TOKEN[:20]}...")
    else:
        print("   ❌ SLACK_BOT_TOKEN이 설정되지 않았습니다.")
        return
    
    if Config.SLACK_TEAM_ID:
        print(f"   ✅ SLACK_TEAM_ID: {Config.SLACK_TEAM_ID}")
    else:
        print("   ⚠️ SLACK_TEAM_ID가 설정되지 않았습니다.")
    
    print()
    
    # 2. Slack 연결 테스트
    print("2. Slack 연결 테스트:")
    if not test_slack_connection():
        print("   Slack 연결에 실패했습니다. 토큰을 확인해주세요.")
        return
    
    print()
    
    # 3. 멤버 정보 가져오기
    print("3. 멤버 정보 가져오기:")
    members = get_slack_members()
    
    if members is None:
        print("   ❌ 멤버 정보를 가져올 수 없습니다.")
        return
    
    print(f"   ✅ 총 {len(members)}명의 멤버를 찾았습니다.")
    print()
    
    # 4. 멤버 정보 출력 (처음 3명만)
    print("4. 멤버 정보 샘플:")
    for i, member in enumerate(members[:3]):
        print(f"   [{i+1}] {member['name']} ({member['email']})")
        print(f"       Slack ID: {member['slack_user_id']}")
        print(f"       아바타: {member['avatar_url']}")
        print()
    
    if len(members) > 3:
        print(f"   ... 그 외 {len(members) - 3}명")
    
    print("=== 테스트 완료 ===")

if __name__ == "__main__":
    main()