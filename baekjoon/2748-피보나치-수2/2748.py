import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")  
    except:
        pass     

# 재귀적 피보나치
def fibo_func(n):  
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibo_func(n - 1) + fibo_func(n - 2)

# 메모이제이션 피보나치
memo = {}
def fibo2_func(n):
    if n <= 1:
        return n
    if n not in memo:
        memo[n] = fibo2_func(n - 1) + fibo2_func(n - 2)

    return memo[n]

# 타볼레이션 피보나치
def fibo3_func(n):
    memo = {}
    
    memo[0] = 0
    memo[1] = 1

    for i in range(2, n + 1):
        memo[i] = memo[i - 1] + memo[i - 2]
    
    return memo[n]

set_io()
input = sys.stdin.readline

n = int(input())

#print(fibo_func(n))

#print(fibo2_func(n))

print(fibo3_func(n))
