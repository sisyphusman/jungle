n = int(input())

for _ in range(n):
    total_point = 0
    sequential_value = 0

    num_str = input()

    for i in range(len(num_str)):
        if num_str[i] == 'O':
            sequential_value += 1
        else:
            sequential_value = 0

        total_point += sequential_value
    
    print(total_point)