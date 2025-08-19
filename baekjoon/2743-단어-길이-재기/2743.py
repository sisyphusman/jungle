import sys

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
    except:
        pass

set_io()
input = sys.stdin.readline

n = int(input())

for _ in range(n):
    lst = list(input().strip())
    print(lst[0]+lst[-1])