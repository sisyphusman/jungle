import sys

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
    except:
        pass

set_io()
input = sys.stdin.readline

n, m = map(int, input().split())

lst = list(range(1, n + 1))

for _ in range(m):
    swap1, swap2 = map(int, input().split())
    temp = lst[swap1- 1]
    lst[swap1 - 1] = lst[swap2 - 1]
    lst[swap2 - 1] = temp

for var in lst:
    print(var, end= " ")