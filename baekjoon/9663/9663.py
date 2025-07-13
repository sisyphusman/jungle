# n 입력값 = 체스판 n x n, 퀸의 수 n
# 퀸이 서로 공격 할 수 없게 놓을 수 있는 경우의 수

# 범위 체크하는 함수

# 사용 여부 체크 리스트




n = int(input())

board = [[0 for _ in range(n)] for _ in range(n)]

for row in board:
    print(*row)
