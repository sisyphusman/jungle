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

# 스택을 활용한 넓이 구하기

def histogram(N, lst):
    stack = []
    answer = 0
    lst.append(0)                                       # list 맨 뒤에 0을 추가 (pop되지 않은 채 남아있는 경우를 제거, 1~5 일때 pop되지 않음)

    for i in range(N+1):
        value = lst[i]                                  # 현재 막대의 높이
        start = i                                       # 시작 인덱스 (왼쪽 경계)

                                                        # 스택에 값이 있고, 현재 값이 스택의 TOP보다 작으면 직사각형 확장을 종료
        while stack and stack[-1][1] >= value:          # 지금 막대보다 높이가 낮은 막대들은 스택에 나두고 나중에 확장을 함
            start, height = stack.pop()                 # 맨 마지막 막대기를 뺀다
            answer = max(answer, (i - start) * height)  # 이전에 저장된 넓이와 비교한다 (현재 인덱스에서 팝된 막대기의 시작 인덱스를 빼고) * 높이를 곱함
        
        stack.append([start, value])                    # 현재 막대기의 인덱스와 높이를 스택에 저장

    print(answer)                                       # 마지막까지 다 했다면 결과를 출력

def main():
    set_io()

    while True:
        lst = get_int_list()

        if lst[0] == 0:
            break

        histogram(lst[0], lst[1:])

if __name__ == "__main__":
    main()