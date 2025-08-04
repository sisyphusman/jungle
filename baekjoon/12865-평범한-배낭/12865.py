import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

set_io()
input = sys.stdin.readline

N, K = map(int, input().split())

lst = [[0,0]]       # 0번은 더미
dp = [[0] * (K + 1) for _ in range(N + 1)]

# 각 물건의 무게와 가치를 입력받아 리스트에 저장
for i in range(N):
    w, v = map(int, input().split())
    lst.append([w, v])
    
# DP (i = 물건의 번호, j = 무게 용량)
for i in range(1, N + 1):                                       # 1번째 물건부터 N번째 물건까지
    for j in range(1, K + 1):                                   # 배낭 용량 1부터 K까지 고려
        w = lst[i][0]                                           # i 번째 물건의 무게
        v = lst[i][1]                                           # i 번째 물건의 가치
                        
        if j < w:                                               # 현재 배낭 용량(j)이 i번째 물건 무게(w)보다 작으면 넣지 못함
            dp[i][j] = dp[i - 1][j]                             # 이전 상태 유지
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w] + v)  # 물건을 넣을 수 있는 경우
                                                                # 1. 안 넣는 경우: dp[i-1][j]
                                                                # 2. 넣을 수 있는 경우: dp[i-1][j-w] + v
                                                                # 둘 중 최대 가치를 선택
print(dp[N][K])