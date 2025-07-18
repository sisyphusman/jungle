import sys

def set_io():
    try:
        sys.stdin = open('input.txt','r')
        sys.stdout = open('output.txt','w')

    except:
        pass

def input(): return sys.stdin.readline().strip()
def get_int(): return int(input())
def get_ints(): return map(int, input().split())
def get_int_list(): return list(get_ints)
def get_str_list(): return list(input().split())

# 거리 값을 받은 이후에 순회하면서 몇개 삽입 가능한지 카운트

def cal_count(arr, mid):
    # 처음 집은 무조건 포함
    count = 1 
    j = 0

    # 첫집-두번째집부터 검사하는데, 두번째 집을 찾으면 그 집을 기준으로 다시 검사
    for i in range(1, len(arr)):
        if arr[i] - arr[j] >= mid:
            count += 1
            j = i

    return count

# left는 최소 거리
# right는 최대 거리
def binary_search(arr, target, left, right):
    max_num = 0
    while left <= right:
        
        # mid를 공유기간 거리라고 가정
        mid = (left + right) // 2

        count = cal_count(arr, mid)

        # 설치 가능하면(left -> mid 이동) 더 큰 거리로 다시 탐색
        if count >= target:
            max_num = max(max_num, mid)
            left = mid + 1
        else:
            right = mid - 1 # 설치 불가능하면 더 작은 거리로 다시 탐색
        
    return max_num


def main():
    set_io()

    n, c = get_ints()
    lst = []
    
    for _ in range(n):
        lst.append(get_int())

    lst.sort()
    
    # 전체 집, 공유기, 최소 거리, 첫 집에서 마지막집간의 거리
    print(binary_search(lst, c, 1, lst[len(lst) - 1] - lst[0]))

if __name__ == '__main__':
    main()