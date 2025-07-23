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

    lst = []
    answer = []
    count = 0

    for i in range(n):
        lst.append(i + 1)

    j = 0
    while True:
        if not lst:
            break

        # 큐 마지막 다음 인덱스이면 나머지 연산으로 0으로 돌아감
        # 마지막 인덱스는 줄어든 수만큼 빼야함
        # j 값에 k만큼 뒤에 있는 인덱스와 배열이기 때문에 - 1
        j = (j + k - 1) % (n - count)
        
        answer.append(lst.pop(j))
        count += 1

    print("<", end= "")
    for var in answer:
        if var == answer[-1]:
            print(var, end = "")
        else:
            print(var, end= ", ")
    print(">", end= "")


if __name__ == "__main__":
    main()