import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

set_io()
input = sys.stdin.readline

n = int(input())
lst = []

for i in range(n):
    a, b = map(int, input().split())
    lst.append((a, b))

# 끝 값 기준으로 정렬 끝 값이 같으면 앞 값 기준으로 정렬
lst.sort(key=lambda x: (x[1], x[0]))

temp = 0
count = 0

for a,b in lst:
    if a >= temp:
        temp = b
        count += 1

print(count)