import sys

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

# A B C
# B D .
# C E F
# E . .
# F . G
# D . .
# G . .

# 전위 순회
def preorder(node, tree):
    if node == ".":
        return
    print(node, end="")
    preorder(tree[node][0], tree)    
    preorder(tree[node][1], tree)

# 중위 순회
def inorder(node, tree):
    if node == ".":
        return
    inorder(tree[node][0], tree)
    print(node, end="")
    inorder(tree[node][1], tree)
    
# 후위 순회
def postorder(node, tree):
    if node == ".":
        return
    postorder(tree[node][0], tree)
    postorder(tree[node][1], tree)
    print(node, end="")

def main():
    set_io()
    n = get_int()
    
    tree = {}

    for _ in range(n):
        parent, left, right = input().split()
        tree[parent] = (left, right)

    preorder('A', tree)
    print()

    inorder('A', tree)
    print()

    postorder('A', tree)

if __name__ == "__main__":
    main()