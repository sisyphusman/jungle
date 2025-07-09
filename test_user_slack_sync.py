#!/usr/bin/env python3
"""
기존 users 컬렉션과 Slack 정보 동기화 테스트
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.slack_helper import sync_slack_to_users
from models.user import get_users_without_slack, get_users_with_slack
from models.database import users_collection

def main():
    print("=== 사용자-Slack 정보 동기화 테스트 ===\n")
    
    # 1. 현재 사용자 상태 확인
    print("1. 현재 사용자 상태 확인:")
    
    # 전체 사용자 수
    total_users = users_collection.count_documents({})
    print(f"   전체 사용자 수: {total_users}명")
    
    # Slack 연동 안된 사용자
    users_without_slack = get_users_without_slack()
    print(f"   Slack 미연동 사용자: {len(users_without_slack)}명")
    
    if users_without_slack:
        print("   미연동 사용자 목록:")
        for user in users_without_slack:
            print(f"     - {user['name']} ({user['email']})")
    
    # Slack 연동된 사용자
    users_with_slack = get_users_with_slack()
    print(f"   Slack 연동 사용자: {len(users_with_slack)}명")
    
    if users_with_slack:
        print("   연동 사용자 목록:")
        for user in users_with_slack:
            print(f"     - {user['name']} ({user['email']}) -> {user['slack_user_id']}")
    
    print()
    
    # 2. Slack 동기화 실행
    print("2. Slack 정보 동기화 실행:")
    result = sync_slack_to_users()
    
    if result['success']:
        print(f"   ✅ {result['message']}")
        print(f"   매칭된 사용자: {result['matched_count']}명")
        print(f"   미매칭 사용자: {result['unmatched_count']}명")
        print(f"   업데이트된 사용자: {result['updated_count']}명")
    else:
        print(f"   ❌ 동기화 실패: {result['message']}")
        return
    
    print()
    
    # 3. 동기화 후 상태 확인
    print("3. 동기화 후 상태 확인:")
    
    users_without_slack_after = get_users_without_slack()
    users_with_slack_after = get_users_with_slack()
    
    print(f"   Slack 미연동 사용자: {len(users_without_slack_after)}명")
    print(f"   Slack 연동 사용자: {len(users_with_slack_after)}명")
    
    if users_with_slack_after:
        print("   연동 완료된 사용자:")
        for user in users_with_slack_after:
            print(f"     - {user['name']} ({user['email']})")
            print(f"       Slack ID: {user['slack_user_id']}")
            print(f"       아바타: {user['avatar_url']}")
            print(f"       동기화 시간: {user['slack_synced_at']}")
            print()
    
    print("=== 테스트 완료 ===")

if __name__ == "__main__":
    main()