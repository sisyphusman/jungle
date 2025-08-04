import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

# 모듈러 연산의 분배 법칙을 활용해서 나머지를 각각 적용을 해서 매 숫자를 작게 만듬
def fibo_func(n):
    memo = {}
    memo[0] = 1
    memo[1] = 1
    for i in range(2, n + 1):
        memo[i] = (memo[i - 1] + memo[i - 2]) % 15746

    return memo[n]

# 피보나치 최적화
def fibo_func2(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, (a + b) % 15746
    
    return b

set_io()
input = sys.stdin.readline

n = input()

print(fibo_func(n))