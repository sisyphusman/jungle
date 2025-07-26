def heap_sort(arr):

    def donw_heap(arr, left, right):
        temp = arr[left]                                                    # 루트 임시 보관
        
        parent = left                                                       # 인덱스 보관
        while parent < (right + 1) // 2:                                    # 자식이 존재할 수 있는 마지막 부모 인덱스
            cl = parent * 2 + 1                                             # 왼쪽 자식
            cr = cl + 1                                                     # 오른쪽 자식
            child = cr if cr <= right and arr[cr] > arr[cl] else cl         # 자식 값은 큰 값을 선택
            if temp >= arr[child]:
                break
            arr[parent] = arr[child]    
            parent = child
        arr[parent] = temp

    arr_size = len(arr)
                                                                    # (arr_size - 1) // 2는 가장 마지막 부모의 노드의 인덱스
    for i in range((arr_size - 1) // 2, -1, -1):                    # 배열의 전체를 최대 힙으로 바꾼다
        donw_heap(arr, i, arr_size - 1)

    for i in range(arr_size - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]                             # 힙의 루트를 맨 뒤로 보냄
        donw_heap(arr, 0, i - 1)

if __name__ == '__main__':
    num = int(input())
    lst = [None] * num

    for i in range(num):
        lst[i] = int(input(f'x[{i}] : '))

    heap_sort(lst)

    for i in range(num):
        print(f'x[{i}] = {lst[i]}')