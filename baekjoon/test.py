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

def sum_array(arr, left, right):
    if left == right:
        return arr[left]

    mid = (left + right) // 2
    left_sum = sum_array(arr, left, mid)        # 왼쪽 절반: left ~ mid 이다
    right_sum = sum_array(arr, mid + 1, right)  # 오른쪽 절반: mid + 1 ~ right이다

    return left_sum + right_sum

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def main():
    set_io()

    arr = get_int_list()
    #print(sum_array(arr, 0, 4))

    print(gcd(12, 13))
    
if __name__ == "__main__":
    main()