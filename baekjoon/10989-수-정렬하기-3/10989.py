import sys

n = int(input())
count = [0] * 10001 # 계수 정렬, 범위가 1부터 10000개, 0 인덱스는 사용 안함

for _ in range(n):
    var = int(sys.stdin.readline())
    count[var] += 1

i = 0
for var in count:    
    for _ in range(var):
        print(i)
    i +=1