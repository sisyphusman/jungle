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

def main():
    set_io()
    
    n = get_int()
    lst = []

    for _ in range(n):
        temp = get_int()
        lst.append(temp)

    max_num = 0
    count = 0

    for var in lst[::-1]:
        if var > max_num:
            max_num = var
            count += 1


    print(count)
    
if __name__ == "__main__":
    main()