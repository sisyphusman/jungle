import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

set_io()
input = sys.stdin.readline

s1 = input().strip()
s2 = input().strip()

dp = [[0] * (len(s2) + 1 ) for _ in range(len(s1) + 1)]

for i in range(1, len(s1) + 1):
    for j in range(1, len(s2) + 1):
        if s1[i - 1] == s2[j - 1]:                      # 문자열이 같으면      
            dp[i][j] = dp[i - 1][j - 1] + 1             # 대각선 위의 값에 +1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # 왼쪽 위쪽중에서 맥스값이 제일 큰 lcs 길이

print(dp[len(s1)][len(s2)]) # 마지막 행렬의 값