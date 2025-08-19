import sys

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
    except:
        pass

set_io()
input = sys.stdin.readline

lst = list(input())
n = int(input())
print(lst[n - 1])