from random import randint
for tc in range(1, 10 + 1):
    if tc == 1:
        a = 1
        b = 1
    elif tc <= 5:
        a = randint(1, 99)
        b = randint(1, 99)
    elif tc <= 8:
        a = randint(1, 9999)
        b = randint(1, 9999)
    elif tc == 9:
        a = 10000
        b = 10000
    elif tc == 10:
        a = 0
        b = 0
    
    
    with open(f"{tc}.in", "w") as f:
        f.write(f"{a} {b}\n")
    
    with open(f"{tc}.sol", "w") as f:
        f.write(f"{a + b}\n")