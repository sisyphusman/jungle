import sys

n = int(input())
lst = []

for _ in range(n):
    var = int(sys.stdin.readline())
    lst.append(var)

lst.sort(reverse=False)

for var in lst:
    print(var)