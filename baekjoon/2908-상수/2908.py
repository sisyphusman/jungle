#두 개의 변수 받아서, 앞뒤 뒤집고, 큰수 출력

a, b = (map(str ,input().split()))

a_rev = a[::-1]
b_rev = b[::-1]

a_num = int(a_rev)
b_num = int(b_rev)

print(max(a_num, b_num))