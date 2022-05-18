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
    result, _ = proc.communicate()
    t = proc.returncode
    if os.path.exists("/proc/" + str(proc.pid)):
        # RIP
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    result = result.decode(encoding="utf8")
    if t != 0 or len(result.strip()) != 1:
        return (VerdictStatus.err, 0.0)

    if result.strip() == "P":
        return (VerdictStatus.accept, 1.0)
    return (VerdictStatus.reject, 1.0)
