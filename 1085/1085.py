x,y,w,h = map(int, input().split())

s1 = x if x < abs(w - x) else abs(w - x)
s2 = y if y < h - y else h - y

result = s1 if s1 < s2 else s2

print(result)

# x,y의 각 길이값과 사각형과의 거리값(w - x와 h - y 구함)을 비교. 가장 작은 값 출력