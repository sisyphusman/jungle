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

# x가 속한 집합의 대표를 찾아주는 함수
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x]) # 한 번 찾은 루트를 중간 노드들에 저장해서 다음부터 더 빠르게 찾기
    return parent[x]

def union(parent, a, b):
    a_root = find(parent, a)
    b_root = find(parent, b)
    if a_root == b_root:
        return False        # 이미 연결되어 있으면 사이클 생김, 두 정점이 같은 그룹(부모가 같다)면 사이클
    parent[b_root] = a_root # 연결
    return True

# 메인 함수
def main():
    set_io()
    
    # 정점, 간선 수 입력
    v, e = get_ints()
    
    edges = []

    for _ in range(e):
        a, b, w = get_ints()
        edges.append((w, a, b))     # (가중치, 정점1, 정점2) 형태로 지정

    # 가중치 기준 정렬
    edges.sort()

    # 유니온 파인드 초기화 자기 자신이 부모로 초기화
    parent = [i for i in range(v + 1)]  # 1-indexed

    mst_weight = 0
    count = 0   # MST에 포함된 간선 수

    for w, a, b in edges:
        if union(parent, a, b):
            mst_weight += w
            count += 1
            if count == v - 1:
                break

    print(mst_weight)

if __name__ == "__main__":
    main()