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

# 규칙 없이 증가하는 수열을 계산

def main():
    set_io()

    n = get_int()
    arr = get_int_list()

    # 수열을 전부 1이라고 가정 (0이면 아무것도 선택하지 않은 수열)
    dp = [1] * n

    # 이전 원소(j)가 기준 원소(i)전까지 검사
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:                     # 이전 원소가 현재 원소보다 작으면 
                dp[i] = max(dp[i], dp[j] + 1)       # 기준원소 i의 dp와 이전 원소들 j의 dp중 큰 값의 +1 한 값과 비교 (마지막 원소)

    print(max(dp))

if __name__ == "__main__":
    main()