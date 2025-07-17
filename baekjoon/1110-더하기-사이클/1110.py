n = int(input())

# 문자열 변환
origin = str()

if n < 10:
    origin = str(0) + str(n)
else:
    origin = str(n)

# 두 자리를 더해주는 함수
def plus(num):

    # temp = 두 자리를 더하고 나온 숫자
    temp = int(num[0]) + int(num[1])
    
    # 10보다 작다면 앞자리에 0을 붙임
    if (temp < 10):
        temp = str(0) + str(temp)

    # num[1] = 이전 숫자 마지막 자리, 리턴형: 문자열
    return (num[1]) + str(temp)[1]

# 0이면 1을 출력
if (n == 0):
    print(1)
else:        
    temp = plus(origin)
    count = 1
        
    while True: 
        if (origin == temp):
            break

        temp = plus(temp)
        count += 1

    print(count)
