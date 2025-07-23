import sys
import heapq

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

    n = get_int()
    
    heap = []

    for _ in range(n):
        temp = get_int()

        # 0일때 배열이 비어있으면 0 출력
        if temp == 0 and not heap:
            print(0)       
        elif temp == 0:                         # 아니면 최대값 출력후 제거
            print(-heapq.heappop(heap))         # 출력때 최소힙에서 나오는 것을 고려해서 부호변경
        else:
            heapq.heappush(heap, -temp)         # 최소힙에서 절대값 높은 것을 최대값으로 저장

if __name__ == "__main__":
    main()