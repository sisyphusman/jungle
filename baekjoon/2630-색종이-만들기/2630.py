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

# 사각형을 나눠서 처리하는 재귀 함수
def divide(paper, start_x, start_y, size, count):
    color = paper[start_x][start_y]

    # 현재 영역이 모두 같은 색인지 확인
    for i in range(start_x, start_x + size):
        for j in range(start_y, start_y + size):
            if paper[i][j] != color:
                half = size // 2
                divide(paper, start_x, start_y, half, count)
                divide(paper, start_x, start_y + half, half, count)
                divide(paper, start_x + half, start_y, half, count)
                divide(paper, start_x + half, start_y + half, half, count)
                return
            
    count[color] += 1

def main():
    set_io()

    lst = []
    n = get_int()

    for _ in range(n):
        lst.append(get_int_list())

    count = [0, 0]

    divide(lst, 0, 0, n, count)

    print(count[0], count[1])

if __name__ == "__main__":
    main()