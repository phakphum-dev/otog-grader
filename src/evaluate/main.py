import os

from DTO.submission import SubmissionDTO
from DTO.evaluate import EvaluateData
from DTO.result import ResultDTO

from constants.osDotEnv import osEnv
from constants.Enums import EvaluateMode

from evaluate import classic, codeforces
from evaluate.verdict.main import getJudgeType

from handle import fileRead
from message import *
import subtask


def evaModeFromStr(mode: str) -> EvaluateMode:
    if mode == "codeforces":
        return EvaluateMode.codeforces

    return EvaluateMode.classic


def start(submission: SubmissionDTO, srcPath: str, isoPath, useControlGroup:bool, onUpdateRuningInCase) -> ResultDTO:
    if osEnv.GRADER_FORCE_TO_MODE != "none":
        evaMode = evaModeFromStr(osEnv.GRADER_FORCE_TO_MODE)
    else:
        evaMode = evaModeFromStr(submission.mode)

    judgeType = getJudgeType(submission.problemId)
    evaData = EvaluateData(submission, srcPath, evaMode, judgeType)

    # ? read substask first
    if os.path.exists(f"./source/{evaData.submission.problemId}/subtask.json"):
        subContent = fileRead(
            f"./source/{evaData.submission.problemId}/subtask.json")
        printHeader("SUBTASK", f"Found custom subtask")
    else:
        subContent = evaData.submission.testcase
    problemTaskData = subtask.compile(subContent)

    if problemTaskData == None:
        return ResultDTO(evaData.submission.id, "Subtask Error", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo...")

    # Invalid number of testcase
    if problemTaskData.maxCase <= 0:
        printFail("GRADER", "Invalid number of testcase.")
        return ResultDTO(evaData.submission.id, "Invalid nCase", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo..")

    if evaMode == EvaluateMode.codeforces:
        return codeforces.evaluate(evaData, isoPath, useControlGroup, onUpdateRuningInCase, problemTaskData.maxCase)
    else:
        return classic.evaluate(evaData, isoPath, useControlGroup, onUpdateRuningInCase, problemTaskData)
