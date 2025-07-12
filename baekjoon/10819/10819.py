# 오름차순 정렬

# 순열 패키지
import itertools

# 근처 숫자들 계산 함수
def Cal(arr):
    length = len(arr)
    total = 0

    for i in range(length - 1):
        total += abs(arr[i] - arr[i + 1])

    return total

n = int(input())

lst = list(map(int,input().split()))

# 순열(순서 배치 가능한 경우의 수들)이 튜플로 저장 -> 리스트
result = list(itertools.permutations(lst))

max = 0
for item in result:
    num = Cal(item)
    max = num if num > max else max 

print(max)