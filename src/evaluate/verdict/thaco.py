from pathlib import Path
import subprocess
import signal
import os
from DTO.testcaseData import TestcaseData
from constants.Enums import VerdictStatus


def getVerdict(testCaseDto: TestcaseData):
    PROBLEM_PATH = f"./source/{testCaseDto.problemId}"
    if not Path(f"{PROBLEM_PATH}/binCheck").is_file():
        return (VerdictStatus.err, 0.0)

    # ifstream inf(argv[1]); Input file
    # ifstream ans(argv[2]); Expected answer
    # ifstream ouf(argv[3]); user answer
    thisCmd = f"{PROBLEM_PATH}/binCheck {PROBLEM_PATH}/{testCaseDto.testCase}.in {testCaseDto.solPath} {testCaseDto.userPath}"
    proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    resultScore, judgeComment = proc.communicate()
    #             ^ not use now...

    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # RIP
    t = proc.returncode

    if t != 0:
        return (VerdictStatus.err, 0.0)  # Judge Error... Bruh

    try:
        resultScore = float(resultScore.strip())
    except:
        return (VerdictStatus.err, 0.0)  # Judge Error... Bruh

    if abs(resultScore - 1.0) <= 1e-4:  # ? if very close to one
        return (VerdictStatus.accept, 1.0)
    elif abs(resultScore) <= 1e-4:  # ? if very close to zero
        return (VerdictStatus.reject, 0)

    return (VerdictStatus.partial, resultScore)
