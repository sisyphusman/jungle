n = int(input())

# 평균값 구한뒤 평균 학생 / 전체 학생 * 100
# 카운터 변수, 평균값 변수

for _ in range(n): 
    student_list = list(map(int, input().split()))
    stdent_num = int(student_list[0])
    student_list.pop(0)

    total_score = 0
    over_num = 0

    # 점수 총합
    for i in range(stdent_num):
        total_score += student_list[i]

    # 평균 구하기
    average_score = total_score / stdent_num

    # 평균 넘는 학생 숫자
    for i in range(0, stdent_num):
        if student_list[i] > average_score:
            over_num += 1

    result = (over_num / stdent_num) * 100

    print(f"{result:.3f}%")