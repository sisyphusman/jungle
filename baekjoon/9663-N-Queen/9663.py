# N-Queen 문제는 크기가 N × N인 체스판 위에 퀸 N개를 서로 공격할 수 없게 놓는 문제이다.

n = int(input())

pos = [0] * n                             # 각 열에서 퀸의 위치를 출력
flag_a = [False] * n                      # 각 행에서 퀸을 배치했는지 체크
flag_b = [False] * (2*n - 1)              # 오른쪽 위 대각선 방향으로 퀸을 배치했는지 체크
flag_c = [False] * (2*n - 1)              # 왼쪽 아래 대각선 방향으로 퀸을 배치했는지 체크
count = 0

# 출력
def put():
    global count
    count += 1

def set(i: int):
    # i열에 알맞는 위치에 퀸을 배치
    for j in range(n):
        if(     not flag_a[j]                   # j행에 퀸을 배치하지 않았으면
            and not flag_b[i + j]               # 오른쪽 대각선
            and not flag_c[n - 1 - i + j]):     # 왼쪽 대각선
            pos[i] = j                          # 퀸을 j행에 배치
            if i == n - 1 :                     # 모든 열에 퀸 배치를 종료
                put()
            else:
                flag_a[j] = flag_b[i + j] = flag_c[n - 1 - i + j] = True        # 행, 대각선들 체크를 표시
                set(i + 1)                                                      # 다음 열에 퀸을 배치
                flag_a[j] = flag_b[i + j] = flag_c[n - 1 - i + j] = False       # 행, 대각선들 체크 해제

set(0)                                      # 0열에 퀸을 배치
print(count)

# i는 열, j는 행
# flag_a[j]는 행 j에 퀸이 있는지 여부

# flag_b[i+j] 각 테이블 위에 우상향 대각선이 지나가는데 대각선 0, 대각선 1, 대각선 2 순으로 대각선 14개까지 나옴 -> i + j
# ex) 1,0과 0,1을 지나는 대각선은 [1]번째 대각선

# 각 테이블 위에 우