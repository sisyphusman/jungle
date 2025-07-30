import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

def get_bfs(start, graph, visited):
    queue = deque()
    queue.append(start)
    visited[start] = True

    count = 0

    while queue:
        now = queue.popleft()

        for neighbor in (graph[now]):
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
                count += 1

    return count

set_io()

input = sys.stdin.readline

computer = int(input())
edges = int(input())

graph = [[] for _ in range(computer + 1)]

for _ in range(edges):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

visited = [False] * len(graph)

print(get_bfs(1, graph, visited))