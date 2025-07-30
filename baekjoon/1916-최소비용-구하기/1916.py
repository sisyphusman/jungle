import sys
import heapq

from collections import defaultdict

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

def dijkstra(start, graph, V):
    # 거리를 무한대로 초기화
    INF = float('inf')
    distance = [INF] * (V + 1)
    distance[start] = 0     # 시작 정점 거리는 0

    pq = []
    heapq.heappush(pq, (0, start)) # (거리, 정점)

    while pq:
        dist, now = heapq.heappop(pq)

        # 이미 더 짧은 거리로 방문한 적이 있으면 무시
        if distance[now] < dist:
            continue

        # 현재 노드와 연결된 이웃 노드들 확인
        for neighbor, cost in graph[now]:
            new_cost = dist + cost
            if new_cost < distance[neighbor]:
                distance[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    return distance

set_io()
input = sys.stdin.readline

graph = defaultdict(list)

n = int(input())
m = int(input())

for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))

start, end = map(int, input().split())

distance = dijkstra(start, graph, n)

print(distance[end])