class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# 리스트 구성
head = Node(1)
second = Node(2)
third = Node(3)

head.next = second
second.next = third
third.next = head  # 원형 연결

# 순환 출력 (3번까지만)
current = head
count = 0
while count < 6:
    print(current.data, end=" -> ")
    current = current.next
    count += 1