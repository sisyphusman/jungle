# 0~9 숫자에 해당하는 9개 리스트 생성

# 3개 값을 받아 곱한 뒤 각 숫자 자리 파싱 후 리스트의 각 자리값을 ++

digit_list = [0] * 10

num = 3
total = 1

for _ in range(num):
    temp = int(input())
    total *= temp

total_str = str(total)

for var in total_str:
    value = int(var)

    match value:
        case 0:
            digit_list[0] += 1
        case 1:
            digit_list[1] += 1
        case 2:
            digit_list[2] += 1
        case 3:
            digit_list[3] += 1
        case 4:
            digit_list[4] += 1
        case 5:
            digit_list[5] += 1
        case 6:
            digit_list[6] += 1
        case 7:
            digit_list[7] += 1
        case 8:
            digit_list[8] += 1            
        case 9:
            digit_list[9] += 1

for var in digit_list:
    print(var)