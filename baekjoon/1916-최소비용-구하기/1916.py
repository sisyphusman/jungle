import sys
from collections import deque

def set_io():
    try:
        sys.stdin = open("input.txt", "r")
        sys.stdout = open("output.txt", "w")
    except:
        pass


set_io()

input = sys.stdin.readline

