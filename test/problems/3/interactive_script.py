# interactive_script.py
import sys
outputPath   = sys.argv[1]
problemDir   = sys.argv[2]
atCase       = sys.argv[3]

with open(outputPath, "r") as f:
    num1, num2 = map(int, f.read().strip().split())

if num1 == 69: # This is the secret number
    print("NOICE")


if num1 != num2:
    print("P")
else:
    print("-")