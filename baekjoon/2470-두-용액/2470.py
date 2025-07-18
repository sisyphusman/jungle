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
def get_int_list(): return list(get_ints())
def get_str_list(): return list(input().split())

# 배열 내 두가지 값을 더해서 0에 가까운 값을 찾는 수 찾기

def two_pointer(arr, left, right):    
    # 0에 가까운 값을 찾았을때 저장해둠
    value = float("inf") 
    ans_left = left
    ans_right = right
    
    # 0과 가까운 값
    target = 0
    
    # 교차하기전까지, 같은 포인터를 비교하면 X
    while(left < right):
        # 양쪽 포인터의 값을 더한다
        sum = arr[left] + arr[right]

        if sum == target:
            return [arr[left], arr[right]]

        elif sum > target:                      # sum이 0보다 크면
            if abs(value) >= abs(sum) :         # sum 0에 가까우면 sum과 인덱스를 저장한다
                value = sum
                ans_left = left
                ans_right = right
            right -= 1
        else:                                   
            if abs(value) >= abs(sum) :
                value = sum
                ans_left = left
                ans_right = right
            left += 1

    return [arr[ans_left], arr[ans_right]]           

def main():
    set_io()

    n = get_int()
    arr = get_int_list()

    arr.sort()

    lst = two_pointer(arr, 0, len(arr) - 1)
    print(lst[0], lst[1])

if __name__ == '__main__':
    main()