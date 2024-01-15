from DTO.testcaseData import TestcaseData
from constants.Enums import VerdictStatus

import subprocess
import os
import signal


def getVerdict(testCaseDto: TestcaseData):
    PROBLEM_PATH = f"./source/{testCaseDto.problemId}"
    thisCmd = f"python3 {PROBLEM_PATH}/interactive_script.py {testCaseDto.userPath} {PROBLEM_PATH}/ {testCaseDto.testCase}"
    proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        result, _ = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        raise Exception("PROBLEM\ninteractive_script.py use too much time (more than 1 minute)")
    
    t = proc.returncode
    if t != 0:
        raise Exception("PROBLEM\ninteractive_script.py return non-zero value")

    if os.path.exists("/proc/" + str(proc.pid)):
        # RIP
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    result = result.decode(encoding="utf8")
    if len(result.strip()) != 1:
        raise Exception(f"PROBLEM\nOutput from interactive_script.py is not valid\nExpected 1 character but got {result.strip()}")

    if result.strip() == "P":
        return (VerdictStatus.accept, 1.0)
    return (VerdictStatus.reject, 1.0)
