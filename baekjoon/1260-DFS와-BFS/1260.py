import sys
from collections import deque

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

# BFS로 출력하는 함수 (edge list -> adj list[인접 리스트] 필요)
def print_bfs(start, graph):
    visited = [False] * len(graph)
    queue = deque()
    queue.append(start)
    visited[start] = True

    while queue:
        now = queue.popleft()
        print(now, end=" ")

        for neighbor in (graph[now]): # 방문 순서를 오름차순으로 정렬
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

# DFS로 출력하는 함수
def print_dfs(start, graph):
    visited = [False] * len(graph)
    stack = []
    
    stack.append(start)

    while stack:        
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            print(node, end=" ")
            # 이웃 노드를 오름차순으로 방문하면 역순 push
            for neighbor in reversed(graph[node]):
                if not visited[neighbor]:
                    stack.append(neighbor)


def main():
    set_io()
    
    n, m , v = get_ints()
    
    nodes = []

    for _ in range(m):
        nodes.append(get_int_list())      
    
    graph = [[] for _ in range(n + 1)]
    for a, b in nodes:
        graph[a].append(b)
        graph[b].append(a)

    for i in range(1, n + 1):
        graph[i].sort()

    print_dfs(v, graph)
    
    print()

    print_bfs(v, graph)

if __name__ == "__main__":
    main()