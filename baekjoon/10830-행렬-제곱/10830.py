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

def mat_pow(a, b):
    if b == 1:                              # b가 1일때 각 원소에 %1000 한 값을 리턴함
        return [[element % 1000 for element in row] for row in a]
    half = mat_pow(a, b // 2)               # 재귀한 값을 저장
    result = mat_mul(half, half)            # 나머지 연산한 결과를 받아옴
    if b % 2 == 1:                          # 홀수이면 한번 곱함
        result = mat_mul(result, a)
    return result

def mat_mul(a, b):
    answer = []
    m, n, r = len(a), len(a[0]), len(b[0])  # a는 크기가 m * n, b의 크기가 n * r

    for i in range(m):
        arr = a[i]
        result = []
        for j in range(r):
            hap = 0
            for k in range(n):
                hap += arr[k] * b[k][j]
                hap %= 1000
            result.append(hap)
        answer.append(result)

    return answer

def main():
    set_io()
    
    lst = []
    n,b = get_ints()

    for _ in range(n):
        lst.append(get_int_list())
    
    ans = mat_pow(lst, b)
    
    for row in ans:
        print(*row)

if __name__ == "__main__":
    main()