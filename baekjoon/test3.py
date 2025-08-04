'''
그래프 - 정점과 간선으로 구성된 자료구조, 방향/무방향, 가중치/비가중치 등으로 구분

트라이 - 문자열을 저장하고 탐색하기 위한 트리 기반 구조, 주로 자동완성, 사전 구현에 사용됨

트리 - 사이클이 없는 연결 그래프, 부모-자식 관계, 이진 트리, 이진 탐색 트리 등이 있음

힙 - 우선 순위 큐 구현에 쓰이는 트리 구조, 최대/최소값을 빠르게 꺼낼 수 있음

BFS(너비 우선 탐색) - 큐를 이용해 가까운 노드부터 탐색, 최단거리 탐색에 유리

DFS(깊이 우선 탐색) - 스택/재귀를 이용해 깊게 탐색, 모든 경로를 확인할때 유리

위상정렬 - 방향 그래프에서 순서를 정할 때 사용, 진입차수가 0 인 노드부터 처리

다익스트라 - 가중치가 있는 그래프에서 최단 경로 탐색, 동적 계획법 활용

플로이드-와샬 - 모든 정점 쌍 간의 최단 거리 탐색, 동적 계획법

최소 신장 트리(MST) - 모든 노드를 최소 비용으로 연결하는 트리(크루스칼, 프림 알고리즘 사용)

동적 프로그래밍(DP) - 큰 문제를 작은 문제로 나눠서 결과를 저장하며 푸는 방식(메모이제이션)

그리디 알고리즘 - 매 순간 최적의 선택을 하는 방식


graph = {
    'A' : ['B', 'C'],
    'B' : ['A', 'D'],
    'C' : ['A', 'D'],
    'D' : ['B', 'C']
}

print(graph['A'])


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

root = TrieNode()

def insert(word):
    node = root
    for char in word:
        node = node.children.setdefault(char, TrieNode())
    node.is_end = True

insert("apple")


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
    
root = Node(1)
root.left = Node(2)
root.right = Node(3)


import heapq

nums = [5, 3, 7, 1]
heapq.heapify(nums)
print(heapq.heappop(nums))


from collections import deque

def bfs(start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            print(node)
            visited.add(node)
            queue.extend(graph[node])

def dfs(node, visited=set()):
    if node not in visited:
        print(node)
        visited.add(node)
        for neighbor in graph[node]:
            dfs(neighbor, visited)

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': [],
    'D': []
}
dfs('A')
bfs('A')
'''
from collections import deque

def topological_sort(V, adj):
    indegree = [0] * V
    for u in adj:
        for v in adj[u]:
            indegree[v] += 1

    queue = deque([i for i in range(V) if indegree[i] == 0])
    result = []

    while queue:
        u = queue.popleft()
        result.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return result

adj = {0: [1, 2], 1: [3], 2: [3], 3: []}
print(topological_sort(4, adj))