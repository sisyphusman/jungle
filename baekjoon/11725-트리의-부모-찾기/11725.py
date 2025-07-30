import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

def bfs(root):
    queue = deque([root])                           # 큐에 root 노드를 넣음
    visited[root] = True

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = current          # 이웃 노드의 부모는 현재 노드다
                queue.append(neighbor)

set_io()
input = sys.stdin.readline

n = int(input())
graph = [[] for _ in range(n + 1)]
parent = [0] * (n + 1)
visited = [False] * (n + 1)

for _ in range(n - 1):                              # 인접 리스트
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)                              # 무방향 그래프

bfs(1)

for i in range(2, n + 1):
    print(parent[i])