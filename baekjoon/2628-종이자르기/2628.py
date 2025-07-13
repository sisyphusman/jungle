# 모든 값들을 받는다

x, y = map(int, input().split())

count = int(input())

p_width = list()
p_height = list()

for _ in range(count):
    cut, p = map(int, input().split())
    
    if cut == 0:
        p_width.append(p)
    else:
        p_height.append(p)

p_width.sort()
p_height.sort()

width = []
height = []

prev = 0    

for item in p_width:
    width.append(item - prev)
    prev = item

width.append(y - prev)

prev = 0

for item in p_height:
    height.append(item - prev)
    prev = item
    
height.append(x - prev)
    

max_val = 0

for val_width in width:
    for val_height in height:
        area = val_width * val_height 
        if area > max_val:
            max_val = area

print(max_val)

# 잘라진 가로, 세로 길이들을 리스트로 만든다
# 가로 세로를 곱한 모든 면적중에서 제일 큰 값을 구한다