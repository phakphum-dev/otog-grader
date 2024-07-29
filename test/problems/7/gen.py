testcases = [5, 4, 3]
tc = 1
for i, testcase in enumerate(testcases):
    for ti in range(testcase):
        c_testcase = tc + ti
        with open(f"{c_testcase}.in", "w") as f:
            f.write(f"{i + 1} {ti + 1}\n")
        with open(f"{c_testcase}.sol", "w") as f:
            f.write("")
    tc += testcase