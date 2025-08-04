import time

# 1 2 3 5 8 13 21 34 55 89 144

# 피보나치 함수의 일반 재귀
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)

# DP 메모이제이션 Top down
def fib2(n, memo={}):
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fib2(n - 1, memo) + fib2(n - 2, memo)
        print(memo)
    return memo[n]

# DP 테이블화(타볼레이션) Bottom up
def fib3(n):
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]

# 0 1 1 2 3 5 8 13 21 34 55 89 144

start = time.time()

#print(fib(37))

#print(fib2(37))

print(fib3(37))

end = time.time()

print(f"실행 시간 : {end - start:.6f} 초")

# 동적 계획법 이름 자체가 왜 ‘Dynamic’인지” - 그럴듯해 보이도록” 만들기 위해 ‘Dynamic’이라는 말을 썼다

# 세 함수 중 가장 빠른 건 무엇이고, 왜 빠를까요?

# 각 함수의 시간 복잡도는?
# 재귀 - 두 개의 재귀 호출 -> O(2ⁿ)
# 메모이제이션 - n개의 서로 다른 입력값만 계산되고, 각 값은 딱 한 번만 계산됨 - O(n)
# 반복문 - dp 배열만큼 사용 O(n)

# Top-down과 Bottom-up 방식의 핵심 차이는 무엇일까요?
# Top-down: 필요한 값만 재귀 + 저장
# Bottom-up: 가장 작은 문제부터 반복문으로 쌓아서 올림

# 메모이제이션 -> 재귀 기반 Top-down
# 테이블화 -> 반복문 기반 Bottom-up