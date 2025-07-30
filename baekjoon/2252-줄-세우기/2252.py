import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

set_io()
input = sys.stdin.readline

N, M = map(int, input().split())

graph = [[] for _ in range(N + 1)]
indegree = [0] * (N + 1)

# 간선 리스트를 만든다
for _ in range(M):
    n, m = map(int, input().split())
    graph[n].append(m)
    indegree[m] += 1

# 위상 정렬을 위한 큐
queue = deque()

# 진입 차수가 0인 노드를 큐에 삽입
for i in range(1, N + 1):
    if indegree[i] == 0:
        queue.append(i)

# 결과
result = []

while queue:
    now = queue.popleft()
    result.append(now)

    for next in graph[now]:
        indegree[next] -= 1
        if indegree[next] == 0:
            queue.append(next)


print(*result)