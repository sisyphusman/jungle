n = int(input())

for i in range(1, 10): #range 객체 반환 끝 숫자 포함 안됨
    print(f"%d * %d = %d" % (n, i, n*i))