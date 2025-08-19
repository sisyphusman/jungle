import sys

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
    except:
        pass

set_io()
input = sys.stdin.readline

lst = list(range(1, 31))

for _ in range(28):
    n = int(input())
    if (lst.count(n)):
        lst.remove(n)

for var in lst:
    print(var)