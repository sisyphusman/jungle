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
def get_int_list(): return list(map(int, input().split()))
def get_str_list(): return list(input().split())

# 배열과 mid값을 각각 빼서 총합을 주는 함수
def tree_total(arr, height):
    total = 0
    for data in arr:
        if (height < data):
            total += data - height
    
    return total

# 이분탐색 부분, 인자 값으로 나무 높이 배열들, 가져가길 원하는 높이, 0부터, 제일 큰 나무까지
def binary_search(arr, target, start, end):
    # 가져갈 수 있는 제일 큰 나무의 값
    max_height = 0
    
    # 0부터 제일 큰 길이의 나무의 값이 교차하지 않을때까지
    while start <= end:
        # 나눈 값이 테스트 해볼 나무의 높이 값
        height = (start + end) // 2

        tree_value = tree_total(arr, height)
        
        if tree_value >= target:
            max_height = max(height, max_height)   
            start = height + 1          
        else:
            end = height - 1

    return max_height

def main():
    set_io()

    n, target = get_ints()
    arr = get_int_list()

    # 제일 큰 나무를 마지막에 배치하기 위해서
    arr.sort()

    print(binary_search(arr, target, 0, arr[len(arr) - 1]))

if __name__ == "__main__":
    main()


# 이분 탐색을 0부터 제일 큰 나무까지의 값으로 한다 (start = 0, end = arr[마지막])
# mid 값은 높이 값이고 이 값을 통해 가져갈 수 있는 나무의 양을 구한다
# 나무의 양이 타켓보다 크면 저장을 해두고, 시작지점(0)을 현재 mid 값보다 크게 잡는다
# 그렇게 해서 나온 제일 큰 높이값을 리턴한다
