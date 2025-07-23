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

def my_stack(lst):
    stack = []
    for c in lst:            
        if c == '(':
            stack.append(c)
        else:
            if len(stack) > 0:
                stack.pop()
            else:
                return False
    if len(stack) > 0:
        return False
    else:
        return True

def main():
    set_io()
    
    n = get_int()
    
    for _ in range(n):
        lst = list(input().strip())
        result = my_stack(lst)

        if result == True:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    main()