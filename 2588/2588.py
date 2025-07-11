a = int(input())
b = int(input())

result = a * b

digit = list(map(int, str(b)))

for i in range(3, 0, -1):
    print(a * digit[i - 1]) 

print(result)