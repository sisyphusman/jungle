import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

def bfs(start):
    queue = deque([start])
    dist[start] = 0

    while queue:
        now = queue.popleft()

        for neighbor in graph[now]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[now] + 1
                queue.append(neighbor)
    
set_io()

input = sys.stdin.readline

n, m, k, x = map(int, input().split())
graph = [[] for _ in range(n + 1)]
dist = [-1] * (n + 1)

for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)

bfs(x)

found = False
for i in range(1, n + 1):
    if dist[i] == k:
        print(i)
        found = True

if not found:
    print(-1)