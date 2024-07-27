from pathlib import Path
import subprocess
import signal
import os
from DTO.testcaseData import TestcaseData
from constants.Enums import VerdictStatus


def getVerdict(testCaseDto: TestcaseData, problemPath: str):
    if not Path(f"{problemPath}/binCheck").is_file():
        raise Exception("PROBLEM\nBinary file not found\n maybe thaco.cpp was compile error")

    # ifstream inf(argv[1]); Input file
    # ifstream ans(argv[2]); Expected answer
    # ifstream ouf(argv[3]); user answer
    thisCmd = f"{problemPath}/binCheck {problemPath}/{testCaseDto.testCase}.in {testCaseDto.solPath} {testCaseDto.userPath}"
    proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    try:
        resultScore, judgeComment = proc.communicate(timeout=60)
        #             ^ not use now...
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        raise Exception("PROBLEM\nthaco.cpp use too much time (more than 1 minute)")

    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # RIP
    t = proc.returncode

    if t != 0:
        raise Exception("PROBLEM\nthaco.cpp return non-zero value")

    try:
        resultScore = float(resultScore.strip())
    except:
        raise Exception(f"PROBLEM\nthaco.cpp return invalid score\nExpected float but got {resultScore.strip()}")

    if abs(resultScore - 1.0) <= 1e-4:  # ? if very close to one
        return (VerdictStatus.accept, 1.0)
    elif abs(resultScore) <= 1e-4:  # ? if very close to zero
        return (VerdictStatus.reject, 0)

    return (VerdictStatus.partial, resultScore)
