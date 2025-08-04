import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

set_io()
input = sys.stdin.readline

T = int(input())

for _ in range(T):
    n = int(input())
    coins = []
    coins = list(map(int, input().split()))
    target = int(input())

    # dp[i] = i원을 만들 수 있는 조합 수 
    dp = [0] * (target + 1)

    # dp[0] 0원을 만드는 방법은 1가지
    dp[0] = 1

    # i가 coin일때 조합수를 계산한 다음 그 결과를
    # 다음 코인에서도 같이 사용
    for coin in coins:
        for i in range(coin, target + 1):
            dp[i] += dp[i - coin]

    print(dp[-1])