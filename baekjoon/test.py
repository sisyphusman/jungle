s = "1 2 3 4"

s = list(map(int, s.split(" ")))
print((str(min(s)) + " " +str(max(s))))