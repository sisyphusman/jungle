lst = []

for _ in range(9):
	var = int(input())
	lst.append(var)

total = sum(lst)

is_done = False

for i in range(len(lst) - 1):
	for j in range(i + 1, len(lst)):
		result = total - (lst[i] + lst[j])
		if result == 100:
			item1, item2 = lst[i], lst[j]
			lst.remove(item1)
			lst.remove(item2)
			is_done = True
			break;

	if is_done:
		break;

lst.sort()

for item in lst:
	print(item)