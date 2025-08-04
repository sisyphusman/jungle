import sys

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass

def cal_total(str):
    total = 0
    temp = str
    idx = 0
    
    f_minus = False

    for i in range(len(temp)):
        if temp[i] == "+" or temp[i] == "-":
            num = int(temp[idx:i])
            if f_minus:
                total -= num
            else:
                total += num

            if temp[i] == "-":
                f_minus = True

            idx = i + 1

    # 마지막 숫자 처리
    if idx  < len(temp):
        num = int(temp[idx:])
        if f_minus:
            total -= num
        else:
            total += num        
    
    return total

set_io()
input = sys.stdin.readline

target = input().strip()
print(cal_total(target))