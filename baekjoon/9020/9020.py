import math

#골드바흐 문제, 두 소수를 찾아서 출력한다. 여러가지 인 경우 두 소수의 차이가 가장 작은 것 출력

# 소수 구하는 함수
def is_prime(var):
    if var < 2 :
        return False
    for i in range(2, int(math.sqrt(var))+1):
        if var % i == 0:
            return False
    
    return True 


count = int(input())

for _ in range(count):
    temp = int(input())
    
    # 제곱근이 아닌 절반부터 검사
    for i in range(temp // 2, 1, -1):

        # 두 수 모두 소수인가?
        if is_prime(i) and is_prime(temp - i):
            print(f"{i} {temp - i}")
            break
