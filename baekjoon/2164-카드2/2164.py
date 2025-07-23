import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open('input.txt', 'r')
        sys.stdout = open('output.txt', 'w')
    except:
        pass

def input(): return sys.stdin.readline().strip()
def get_int(): return int(input())
def get_ints(): return map(int, input().split())
def get_int_list(): return list(map(int, input().split()))
def get_str_list(): return input().split()

class create_deque:
    def __init__(self):
        self.data = deque()
    
    def push(self, num):
        self.data.append(num)

    def left_push(self, num):
        self.data.appendleft(num)
    
    def pop(self):
        return self.data.popleft() if self.data else -1
    
    def top(self):
        return self.data.pop() if self.data else -1
    
    def size(self):
        return len(self.data)
    
    def empty(self):
        return 0 if self.data else 1
    
    def front(self):
        return self.data[0] if self.data else -1
    
    def back(self):
        return self.data[-1] if self.data else -1

def main():
    set_io()
    
    n = get_int()

    my_deque = create_deque()   

    for i in range(n, 0, -1):
        my_deque.push(i)

    while True:
        if my_deque.size() == 1:
            break

        my_deque.top()
        temp = my_deque.top()
        my_deque.left_push(temp)

    print(my_deque.front())

if __name__ == "__main__":
    main()
