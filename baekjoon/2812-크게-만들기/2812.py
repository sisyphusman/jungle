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

def main():
    set_io()
    
    n, k = get_ints()
    number = input()
    
    # 스택은 최종값, 큰 숫자가 뒤에서 발견하면 앞으로 k값만큼 작은 숫자를 밀면서 지움
    stack = []

    # 모든 숫자를 순회하며
    for digit in number:
        while stack and k > 0 and stack[-1] < digit:      # 제거 루틴, 앞 숫자보다 현재 숫자가 크고 제거 기회가 남아 있으면 제거
            stack.pop()                                   # 더 작은 숫자를 제거하고 넣기 때문에 오름차순, while을 돌며 작은 숫자들을 제거함
            k -= 1                                        # 남은 제거 횟수 (지우개)
        stack.append(digit)
    
    # 제거 기회가 남았다면 뒤에서 제거 stack = ['5', '4', '3', '2', '1'], k = 2 그대로 남음
    result = stack[:len(stack) - k]

    print(''.join(result))

if __name__ == "__main__":
    main()