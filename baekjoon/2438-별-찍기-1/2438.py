n = int(input())
for i in range(0, n):
    for _ in range(i+1):
        print("*", end='')
    print("")