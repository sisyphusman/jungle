import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

def start_bfs(x, y):
    queue = deque()
    queue.append((x, y))

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            if 0 <= nx < N and 0 <= ny < M:
                if maze[nx][ny] == 1:
                    # 아직 방문 안 한 곳이면, 거리 저장
                    maze[nx][ny] = maze[x][y] + 1
                    queue.append((nx, ny))
    
    return maze[N-1][M-1]

set_io()
input = sys.stdin.readline

N, M = map(int, input().split())
maze = [list(map(int, list(input().strip()))) for _ in range(N)]

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

print(start_bfs(0, 0))