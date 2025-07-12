import math

n = input()
prime_count = 0

lst = list(map(int, input().split()))

for var in lst:

    if var == 1:
        continue

    is_prime = True
    for i in range(2, int(math.sqrt(var) + 1)):
      
        if var % i == 0:
            is_prime = False
            break   

    if is_prime == True:
        prime_count += 1

print(prime_count)

# 소수는 약수의 곱으로 구성
# 약수 2개는 제곱근보다 클 수 없다
# 제곱근을 기준으로 짝을 이룬다