import sys
sys.setrecursionlimit(10**6)

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

# 전위 순회한걸 리스트로 받는 함수
def get_preorder(arr):
    for line in sys.stdin:
        line = line.strip()
        arr.append(int(line))

# 후위 순회 출력 함수(BST를 재귀적으로 처리)
def build_postorder(start, end, arr):
    if start > end:
        return

    # 부모 루트
    root = arr[start]

    # 다음 루트
    idx = start + 1

    # 오른쪽 서브트리 시작점 찾기 (왼쪽 서브트리 마지막 다음에 조건이 벗어남)
    while idx <= end and arr[idx] < root:
        idx += 1

    # 왼쪽 서브트리 (루트 다음 ~ idx(오른쪽 루트 시작점) - 1)
    build_postorder(start + 1, idx - 1, arr)

    # 오른쪽 서브트리 ( 오른쪽 루트 시작점 ~ 마지막 요소), 오른쪽 서브트리가 없다면 idx = end + 1이 되서 무시
    build_postorder(idx, end, arr)

    # 후위 순회는 좌 -> 우 -> 루트
    print(root)

def main():
    set_io()    

    lst = []
    get_preorder(lst)
    build_postorder(0, len(lst) - 1, lst)

if __name__ == "__main__":
    main()