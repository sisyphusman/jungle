import sys

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
    except:
        pass

set_io()
input = sys.stdin.readline

n = int(input().strip())
total = 0

my_str = input().strip()

for var in my_str:
    total += int(var)

print(total)