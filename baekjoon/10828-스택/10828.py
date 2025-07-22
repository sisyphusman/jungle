import sys

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
        sys.stdout = open('output.txt', 'w')
    except:
        pass

def input(): return sys.stdin.readline().strip()
def get_int(): return int(input())
def get_ints(): return map(int, input().split())
def get_int_list(): return list(map(int, input().split()))
def get_str_list(): return input().split()

data = []

def main():
    set_io()
    
    n = get_int()
    for _ in range(n):
        lst = get_str_list()
        if lst[0] == "push":
            data.append(lst[1])
        elif lst[0] == "pop":
            if len(data) > 0:
                print(data.pop())
            else:
                print(-1)
        elif lst[0] == "top":
            print(data[-1] if len(data) > 0 else -1)
        elif lst[0] == "size":
            print(len(data))
        elif lst[0] == "empty":
            print(1 if len(data) == 0 else 0)
        elif lst[0] == "peek":
            if len(data) > 0:
                print(data[-1])
            else:
                print(-1)

if __name__ == "__main__":
    main()