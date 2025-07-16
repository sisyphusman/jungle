import sys
sys.setrecursionlimit(1000000)

# visited = 방문 플래그
# lst = height 높이 정보

def dfs(x, y, visited, lst, n, height):
    visited[x][y] = True                        # 방문 표시

    # 4방향 탐색
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    # 상하좌우 한번씩 이동
    for i in range(4):
        nx = x + dx[i]                          # 좌표 이동한 이후 값 nx, ny
        ny = y + dy[i]

        # x,y 범위를 0에서 n 이전까지 제한
        if 0 <= nx < n and 0 <= ny < n:
            if not visited[nx][ny] and lst[nx][ny] > height:
                dfs(nx, ny, visited, lst, n, height)

def count_safe_areas(lst, n, height):
    visited = [[False] * n for _ in range(n)]
    count = 0

    # 0부터 n까지 모든 시도
    for i in range(n):
        for j in range(n):
            
            # lst의 높이가 기준보다 높고, 방문한적이 없다면
            if lst[i][j] > height and not visited[i][j]:

                # 이어진 지역을 visited = true로 만들기
                dfs(i, j, visited, lst, n, height)

                # 높이가 기준보다 높고, 방문한적 없는 곳을 들렸다면 +1, 그리고 이어진 곳 체크함
                count += 1
    
    return count


n = int(input())
lst = []

for _ in range(n):
    lst.append(list(map(int, input().split())))

#최대 높이 구하기
max_height = 0
for i in range(n):
    for j in range(n):
        max_height = max(lst[i][j], max_height)

max_safe_areas = 0

# 높이 0부터 최대 높이 포함 모든 경우 확인
for height in range(max_height + 1):
    safe_areas = count_safe_areas(lst, n, height)
    max_safe_areas = max(max_safe_areas, safe_areas)

print(max_safe_areas)