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

        if temp != 0:
            lst.append(temp)
        else:
            lst.pop()
    

    result = 0
    if len(lst) != 0:
        for i in range(len(lst)):            
            result += lst[i]
    
    print(result)


if __name__ == "__main__":
    main()