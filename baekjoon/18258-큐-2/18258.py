import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
        #sys.stdout = open('output.txt', 'w')
    except:
        pass

def input(): return sys.stdin.readline().strip()
def get_int(): return int(input())
def get_ints(): return map(int, input().split())
def get_int_list(): return list(map(int, input().split()))
def get_str_list(): return input().split()


def main():
    set_io()
    
    n = get_int()
    data = deque()

    for _ in range(n):
        lst = get_str_list()
        if lst[0] == "push":
            data.append(lst[1])
        elif lst[0] == "pop":
            print(data.popleft() if data else -1)
        elif lst[0] == "top":
            print(data[-1] if data else -1)
        elif lst[0] == "size":
            print(len(data))
        elif lst[0] == "empty":
            print(0 if data else 1)
        elif lst[0] == "front":
            print(data[0] if data else -1)
        elif lst[0] == "back":
            print(data[-1] if data else -1)

if __name__ == "__main__":
    main()

# 리스트의 pop()은 삭제 후 요소를 하나씩 다 옫겨야 하므로 O(N)

# deque는 포인터만 이동하면 되므로 O(1)