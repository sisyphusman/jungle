def solution(numbers, target):
    answer = 0

    def dfs(idx, current_sum):
        nonlocal answer

        # 모든 숫자를 사용한 경우
        if idx == len(numbers):
            if current_sum == target:
                answer += 1
            return
        
        # 다음 숫자를 더하는 경우
        dfs(idx + 1, current_sum + numbers[idx])
        
        # 다음 숫자를 빼는경우
        dfs(idx + 1, current_sum - numbers[idx])

    dfs(0, 0)
    return answer