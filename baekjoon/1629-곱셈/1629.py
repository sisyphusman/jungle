import sys

def set_io():
    try:   
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass
        
def input(): return sys.stdin.readline().strip()
def get_int(): return int(input())
def get_ints(): return map(int, input().split())
def get_int_list(): return list(map(int, input().split()))
def get_str_list(): return list(input().split())

def main():
    set_io()

    a, b, c = get_ints()
    
    # (a*b)%c = ((a%c)*(b%c)) %c

    ac = a%c
    bc = b%c
    total = (ac * bc)%c

    print(total)

if __name__ == "__main__":
    main()