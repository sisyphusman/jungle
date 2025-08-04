import sys
sys.stdin = open("input.txt", "r")
N = int(input())
dp = [[0] * N for _ in range(N)]
matrix = [list(map(int, input().split())) for _ in range(N)]
#
for length in range(1, N):  # 구간 길이
    for i in range(N - length):
        j = i + length
        dp[i][j] = float('inf')
        for k in range(i, j):
            cost = dp[i][k] + dp[k+1][j] + matrix[i][0] * matrix[k][1] * matrix[j][1]
            dp[i][j] = min(dp[i][j], cost)
#
print(dp)





