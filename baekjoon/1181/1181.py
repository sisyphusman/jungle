n = int(input())

lst = [input() for _ in range(n)]

# 중복 제거 후, 길이 -> 사전순 정렬
# sorted() 나 .sort() 는 key 함수가 반환하는 값을 기준으로 오름차순 정렬
# 이 key 함수는 정렬할 각 요소 x에 대해 튜플 (len(x), x) 를 반환
# 첫 번째 요소들을 비교 → 다르면 이걸로 정렬 결정
# 첫 번째 요소들이 같으면 → 두 번째 요소들을 비교

lst = sorted(set(lst), key=lambda x: (len(x), x))

for word in lst:
    print(word)