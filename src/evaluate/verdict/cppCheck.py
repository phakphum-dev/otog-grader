from pathlib import Path
import subprocess
import signal
import os
from DTO.testcaseData import TestcaseData
from constants.Enums import VerdictStatus
from message import *


def getVerdict(testCaseDto: TestcaseData, problemPath: str):
    if not Path(f"{problemPath}/binCheck").is_file():
        raise Exception("PROBLEM\nBinary file not found\n maybe check.cpp was compile error")

    os.system(f"cp {testCaseDto.userPath} ./output.txt")
    thisCmd = f"{problemPath}/binCheck {testCaseDto.solPath} {problemPath}/{testCaseDto.testCase}.in {testCaseDto.srcPath}"
    proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        raise Exception("PROBLEM\ncheck.cpp use too much time (more than 1 minute)")

    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # RIP
    t = proc.returncode

    if t != 0:
        raise Exception(f"PROBLEM\ncheck.cpp return non-zero value (return code: {t})")

    # ? check is grading result file exist
    if not Path("./grader_result.txt").is_file():
        raise Exception("PROBLEM\ngrader_result.txt not found")

    with open("./grader_result.txt", "r") as f:
        result = f.read()

    try:
        os.system("rm ./output.txt")
        os.system("rm ./grader_result.txt")
    except:
        pass

    if len(result.strip()) != 1:
        raise Exception(f"PROBLEM\ngrader_result.txt is not valid\nExpected 1 character but got {result.strip()}")
    if result.strip() == "P":
        return (VerdictStatus.accept, 1.0)
    return (VerdictStatus.reject, 1.0)
