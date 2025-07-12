# 한자리 수이면 무조건 한수
# 두자리 수이면 25 -> 2 - 5 = -3 등차가 하나뿐이므로 한수

def get_num_seq(num):
    digits = [int(d) for d in str(num)]

    # 뒷자리에서 앞자리 뺀것이 격차
    diff =  digits[1] - digits[0]

    # 인덱스 범위 예외 처리
    for i in range(len(digits) - 1):
        # 격차가 하나라도 아니면 false 종료
        if digits[i + 1] - digits[i] != diff:
            return False
        
    return True

n = int(input())

if n <= 99:
    print(n)
else:
    count = 99
    
    #세자리 숫자일때, 100부터 해당 숫자까지 검사
    for i in range(100, n + 1):
        if get_num_seq(i):
            count += 1
    
    print(count)

