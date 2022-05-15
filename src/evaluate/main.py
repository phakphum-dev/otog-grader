from pathlib import Path
import subprocess, os, signal

from DTO.submission import SubmissionDTO
from DTO.evaluate import EvaluateData
from DTO.result import ResultDTO

from constants.Enums import EvaluateMode, JudgeType

from evaluate import classic, codeforces

from handle import fileRead
from message import *
import subtask

def evaModeFromStr(mode: str) -> EvaluateMode:
    if mode == "codeforces":
        return EvaluateMode.codeforces
    
    return EvaluateMode.classic

def getJudgeType(problemId: int) -> JudgeType:
    PROBLEM_PATH = f"./source/{problemId}"

    if Path(f"{PROBLEM_PATH}/interactive_script.py").is_file():
        return JudgeType.ogogi
    if Path(f"{PROBLEM_PATH}/check.cpp").is_file():
        thisCmd = f"g++ {PROBLEM_PATH}/check.cpp -O2 -std=c++17 -fomit-frame-pointer -o {PROBLEM_PATH}/binCheck"
        proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid)
        proc.communicate()
        if os.path.exists("/proc/" + str(proc.pid)):
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # RIP
        return JudgeType.cppCheck

    return JudgeType.standard

def start(submission: SubmissionDTO, srcPath: str, isoPath, onUpdateRuningInCase) -> ResultDTO:
    evaMode = evaModeFromStr(submission.mode)
    judgeType = getJudgeType(submission.problemId)
    evaData = EvaluateData(submission, srcPath, evaMode, judgeType)

    #? read substask first
    if os.path.exists(f"./source/{evaData.submission.problemId}/subtask.tc"):
        subContent = fileRead(f"./source/{evaData.submission.problemId}/subtask.tc")
        printHeader("SUBTASK", f"Found custom subtask")
    else:
        subContent = evaData.submission.testcase
    mxCase, subtaskData = subtask.compile(subContent)

    if mxCase == -1:
        printFail("SUBTASK", f"Subtask error : {subtaskData}")
        return ResultDTO(evaData.submission.id, "Judge Error", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo...\n\n\n{subtaskData}")

    # Invalid number of testcase
    if mxCase <= 0:
        printFail("GRADER", "Invalid number of testcase.")
        return ResultDTO(evaData.submission.id, "Invalid nCase", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo..")

    if evaMode == EvaluateMode.codeforces:
        return codeforces.evaluate(evaData, isoPath, onUpdateRuningInCase, mxCase)
    else:
        return classic.evaluate(evaData, isoPath, onUpdateRuningInCase, subtaskData)
