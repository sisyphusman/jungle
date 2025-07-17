def cal_sum(n, sum = 0, depth = 0):
    if sum == n:
        return 1
    if sum > n:
        return 0
    
    count = 0
    for num in [1, 2, 3]:
        count += cal_sum(n, sum + num, depth + 1)
    
    return count

n = int(input())

for _ in range(n):
    input_value = int(input())
    print(cal_sum(input_value))

# 재귀 함수 만들기
# 1. cal_sum() -> 필요한 인수는 어떻게 설계하는가?
# 2. 탈출 조건은 어떻게 만들것이면 어떤 값을 리턴할것인가?
# 3. 내부 로직은 어떻게 동작하게 할것인가?