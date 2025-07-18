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

# 이분 탐색
def binary_search(array, target, start, end):
    while start <= end:
        mid = (start + end) // 2

        if array[mid] == target:
            return True
        elif array[mid] > target:
            end = mid - 1
        else:
            start = mid + 1

    return False

def main():
    set_io()
    
    n = get_int()
    arr = get_int_list()
    m = get_int()
    arr2 = get_int_list()

    arr.sort()
    
    for data in arr2:
        result = binary_search(arr, data, 0, len(arr) - 1)
        if result:
            print(1)
        else:
            print(0)
    
if __name__ == "__main__":
    main()