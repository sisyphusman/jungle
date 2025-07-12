def generate_permutations(arr, path, used, result):
    if len(path) == len(arr):
        result.append(path[:])
        return

    for i in range(len(arr)):
        if arr[i] == 0:
            break
        if not used[i]:
            used[i] = True
            path.append(arr[i])
            generate_permutations(arr, path, used, result)
            path.pop()
            used[i] = False

# 사용 예시
arr = [1, 2, 3, 0]
result = []
used = [False] * len(arr)

generate_permutations(arr, [], used, result)

for perm in result:
    print(perm)