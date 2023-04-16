from pathlib import Path
import subprocess
import signal
import os
from DTO.testcaseData import TestcaseData
from constants.Enums import VerdictStatus
from message import *


def getVerdict(testCaseDto: TestcaseData):
    PROBLEM_PATH = f"./source/{testCaseDto.problemId}"
    if not Path(f"{PROBLEM_PATH}/binCheck").is_file():
        return (VerdictStatus.problemErr, 0.0)

    os.system(f"cp {testCaseDto.userPath} ./output.txt")
    thisCmd = f"{PROBLEM_PATH}/binCheck {testCaseDto.solPath} {PROBLEM_PATH}/{testCaseDto.testCase}.in {testCaseDto.srcPath}"
    proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        proc.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        printFail("PROBLEM", "check.cpp use too much time (more than 20s)")
        return (VerdictStatus.problemErr, 0.0)

    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # RIP
    t = proc.returncode

    # ? check is grading result file exist
    if not Path("./grader_result.txt").is_file():
        printFail("PROBLEM", "grader_result.txt not found")
        return (VerdictStatus.problemErr, 0.0)

    with open("./grader_result.txt", "r") as f:
        result = f.read()

    try:
        os.system("rm ./output.txt")
        os.system("rm ./grader_result.txt")
    except:
        pass

    if t != 0 or len(result.strip()) != 1:
        return (VerdictStatus.problemErr, 0.0)  # Judge Error... Bruh
    if result.strip() == "P":
        return (VerdictStatus.accept, 1.0)
    return (VerdictStatus.reject, 1.0)
