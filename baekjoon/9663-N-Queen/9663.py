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
        temp = n - 1 - i + j
        if(     not flag_a[j]                   # j행에 퀸을 배치하지 않았으면
            and not flag_b[i + j]               # 오른쪽 대각선
            and not flag_c[temp]):     # 왼쪽 대각선
            pos[i] = j                          # 퀸을 j행에 배치
            if i == n - 1 :                     # 모든 열에 퀸 배치를 종료
                put()
            else:
                flag_a[j] = flag_b[i + j] = flag_c[temp] = True        # 행, 대각선들 체크를 표시
                set(i + 1)                                                      # 다음 열에 퀸을 배치
                flag_a[j] = flag_b[i + j] = flag_c[temp] = False       # 행, 대각선들 체크 해제

set(0)                                      # 0열에 퀸을 배치
print(count)

# i는 열, j는 행
# flag_a[j]는 행 j에 퀸이 있는지 여부

# flag_b[i+j] 각 테이블 위에 우상향 대각선이 지나가는데 대각선 0, 대각선 1, 대각선 2 순으로 대각선 14개까지 나옴 -> i + j
# ex) 1,0과 0,1을 지나는 대각선은 [1]번째 대각선

# 각 테이블 위에 우하향 대각선이 지나가는데, 왼쪽 하단부터 0 대각선으로 시작
# ex) 0,0을 지나는건 대각선 [7]번째 -> (0, 0) -> (1, 1) -> (2, 2) = 7 -> i-j+7 (8x8)

# i와 j를 부호를 반전해도 최소범위~최대값 이내, flag 배열 인덱싱 순서만 바뀜
# 15의 경우 범위가 -14~14인데 이를 0~28로 범위 정규화 하면서 2n-1개의 대각선용 플래그 배열이 필요함 (배열은 음수 인덱스가 x)