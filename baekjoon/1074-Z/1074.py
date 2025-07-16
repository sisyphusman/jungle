def z(n, r, c, count):
    if n == 2:  # 2×2 크기에서 직접 계산
        if r == 0 and c == 0:
            return count
        elif r == 0 and c == 1:
            return count + 1
        elif r == 1 and c == 0:
            return count + 2
        else:
            return count + 3                                                                
    
    mid = n // 2                 # 분면 나눔
    
    if r < mid and c < mid:      # 2사분면             
        return z(mid, r, c, count)
    elif r < mid and c >= mid:   # 1사분면            
        return z(mid, r, c - mid, count + mid * mid)
    elif r >= mid and c < mid:   # 3사분면             
        return z(mid, r - mid, c, count + mid * mid * 2)
    else:                        # 4사분면
        return z(mid, r - mid, c - mid, count + mid * mid * 3)
    
n, row, col = map(int, input().split())
print(z(2**n, row, col, 0))
