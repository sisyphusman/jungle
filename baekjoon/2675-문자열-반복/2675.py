n = int(input())

for _ in range(n):
    # 매 줄마다 인덱스와 스트링 값을 받는다
    m, qr = input().split()       
    # 인덱스 조정 값
    i = 0
    # 문자열의 개수만큼 출력
    for _ in range(len(qr)): 
        # 같은 문자 반복할 횟수
        for _ in range(int(m)):
            print(qr[i], end="")
        
        i += 1
    print("")