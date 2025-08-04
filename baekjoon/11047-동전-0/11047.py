import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

# 큰 값부터 검사하는데 나눈 몫만큼 count 증가, temp 값은 그만큼 빠진 후 다시 검사
def my_count(target):
    count = 0

    temp = target

    for var in reversed(lst):
        if var <= temp:
            divide = int(temp / var)
            count += divide
            temp -= var * divide

    return count

set_io()
input = sys.stdin.readline

N, K = map(int, input().split())

lst = []

for _ in range(N):
    temp = int(input())
    lst.append(temp)

print(my_count(K))

