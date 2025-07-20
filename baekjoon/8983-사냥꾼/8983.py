import sys
import bisect

def set_io():
    try:   
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass
        
def input(): return sys.stdin.readline().strip()
def get_int(): return int(input())
def get_ints(): return map(int, input().split())
def get_int_list(): return list(map(int, input().split()))
def get_str_list(): return list(input().split())


def main():
    set_io()

    # m = 사대의 수, n = 동물의 수, l = 사정거리
    m, n, l = get_ints()
    gun_list = get_int_list()
    
    gun_list.sort()  # 이분탐색을 위한 정렬
    animal_list = []

    count = 0

    for _ in range(n):
        animal_list.append(get_int_list())
    
    for i in range(len(animal_list)):
        left = 0
        right = len(gun_list) - 1                                                   # 포탑 리스트를 이분 탐색
        while left <= right :
            mid = left + (right - left) // 2                                        # (right + left) / 2이랑 같음
            distance = abs(gun_list[mid] - animal_list[i][0]) + animal_list[i][1]   # 동물과 포탑의 상대 거리
            if (distance <= l):                                                     # 포탑 사정거리 이내면
                count += 1                                                          # 죽는 동물 카운트
                break
            else:
                if (animal_list[i][0] >= gun_list[mid]):                            # 동물 좌표가 이분 탐색보다 크면
                    left = mid + 1                                                  # 왼쪽을 미드 + 1로 이동
                else:
                    right = mid - 1                                                 # 오른쪽을 미드 -1로 이동

    print(count)

if __name__ == "__main__":
    main()