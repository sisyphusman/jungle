from itertools import permutations

N = int(input())
data = []
for i in range(N):
    temp = list(map(int, input().split()))
    data.append(temp)

def cal(lst):
    cities = [city for city in range(N)]
    min_cost = float('inf')
    for p in permutations(cities):
        permu = list(p)              # 첫 순열을 리스트로
        permu.append(p[0])           # p[0], 즉 시작지점이 permu로 끝으로 가야된다
        cost = 0
        for n in range(N):           # 0부터 N-1까지
            i = permu[n]             # 순열 리스트의 0부터
            j = permu[n + 1]         # i의 다음 인덱스부터
            
            if lst[i][j] == 0:       # 만약 방문 비용이 0이면? 갈 수 없는 곳
                cost = float('inf')  # 불가능한 경로는 비용이 무한대 -> 절대 선택 X
                break
            
            cost += lst[i][j]        # i에서 j 방문 비용
        min_cost = min(min_cost, cost)

    print(min_cost)


cal(data)
