import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
        sys.stdout = open('output.txt', 'w')
    except:
        pass


def get_bfs(start, graph, visited):
    queue = deque()
    queue.append(start)
    visited[start] = True

    while queue:
        now = queue.popleft()
       #print(now, end =" ")

        for neighbor in (graph[now]):
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

set_io()

input = sys.stdin.readline

n, m = map(int, input().split()) # 정점 수, 간선 수
graph = [[] for _ in range(n + 1)] # 인접 리스트 초기화(1번 노드부터 시작)

for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

count = 0
visited = [False] * len(graph)

for i in range(1, len(visited)):
    if visited[i] == False:
        get_bfs(i, graph, visited)
        count += 1

print(count)