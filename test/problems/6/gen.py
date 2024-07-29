n = 5
for i in range(n):
    with open(f"./{i + 1}.in", "w") as f:
        f.write(f"{i + 1}\n")
    
    with open(f"./{i + 1}.sol", "w") as f:
        f.write(f"")
