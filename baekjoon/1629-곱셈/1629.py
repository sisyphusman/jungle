import sys

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

# a의 b제곱을 하는 재귀 함수
def my_pow(a, b, mod):
    if b == 0:
        return 1
    
    half = my_pow(a, b // 2, mod)           # 지수를 1/2 한 것을 다시 pow한다 (재사용), 짝수 결과 = half -> 홀수에서 재사용
    result = (half * half) % mod            # (a * b) % c = ((a % c) * (b % c)) % c -> (a * a) % c

    if b % 2 == 1:
        result = (result * a) % mod         # a^8 = (a^4)^2,  a^7 = a * (a^3)^2
    
    return result

def main():
    set_io()

    a, b, c = get_ints()   

    print( my_pow(a,b,c))

if __name__ == "__main__":
    main()