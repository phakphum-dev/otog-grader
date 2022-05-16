import os

from DTO.evaluate import EvaluateData
from DTO.result import ResultDTO
from constants.Enums import VerdictStatus
from handle import error
from constants.osDotEnv import *
import cmdManager as langCMD
from evaluate.verdict.main import excuteAndVerdict
from constants.verdict import verdictsColorSymbol, verdictCodeforces, verdictsColorCodeforces

from message import *


def evaluate(evaData: EvaluateData, isoPath: str, onUpdateRuningInCase: str, mxCase: int) -> ResultDTO:

    submission = evaData.submission

    printHeader("Codeforces", f"Evaluate with Codeforces standard")
    printHeader("GRADER", f"use {evaData.judgeType.value} Judge...")
    printHeader("GRADER", f"Runtime process:")

    print("\t-> Result: ", end="", flush=True)
    result = "Accepted"
    resultTime = 0
    resultMem = 0

    realTimeFactor = langCMD.get(
        submission.language, "timeFactor") * float(osEnv.GRADER_TIME_FACTOR)
    testTimeLimit = submission.timeLimit * realTimeFactor

    for testcaseNum in range(1, mxCase+1):

        testcaseResult = excuteAndVerdict(
            submission.problemId,
            testcaseNum,
            testTimeLimit,
            (submission.memoryLimit) * 1024,
            submission.language,
            evaData.srcPath,
            isoPath,
            evaData.judgeType
        )

        resultTime = max(resultTime, testcaseResult.timeUse *
                         1000 // realTimeFactor)
        resultMem = max(resultMem, testcaseResult.memUse)

        result = verdictCodeforces(
            testcaseResult.status).replace("%d", str(testcaseNum))

        if testcaseResult.status != VerdictStatus.accept:
            print(verdictsColorCodeforces(testcaseResult.status).replace(
                "%d", str(testcaseNum)), flush=True)
            return ResultDTO(submission.id, result, 0, resultTime, resultMem, None)

        onUpdateRuningInCase(submission.id, testcaseNum)

    # ? mean accept every testcase
    print(verdictsColorCodeforces(VerdictStatus.accept), flush=True)
    return ResultDTO(submission.id, result, submission.maxScore, resultTime, resultMem, None)
