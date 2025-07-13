n, base_value = map(int, input().split())
temp = list(map(int, (input().split())))

for i in range(n):    
    if temp[i] < base_value:
        print(temp[i], end=" ")