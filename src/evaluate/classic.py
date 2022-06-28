import os

from DTO.evaluate import EvaluateData
from DTO.result import ResultDTO
from DTO.subtask import ProblemTaskDTO, SubtaskDTO
from handle import error
from checkType import *
import cmdManager as langCMD
from constants.osDotEnv import *
from constants.Enums import VerdictStatus
from constants.verdict import verdictSymbol, verdictsColorSymbol

from evaluate.verdict.main import excuteAndVerdict

from message import *


def evaluate(evaData: EvaluateData, isoPath: str, onUpdateRuningInCase: str, subtaskData: ProblemTaskDTO) -> ResultDTO:

    submission = evaData.submission

    printHeader("GRADER", f"use {evaData.judgeType.value} Judge...")
    printHeader("GRADER", f"Runtime process:")

    print("\t-> Result: ", end="", flush=True)
    isPass = [False for i in range(len(subtaskData.orderIndSubtask) + 5)]
    result = ["" for i in range(len(subtaskData.orderIndSubtask) + 5)]
    score = 0
    mxScore = 0
    sumTime = 0
    mxMem = None

    realTimeFactor = langCMD.get(
        submission.language, "timeFactor") * float(osEnv.GRADER_TIME_FACTOR)
    testTimeLimit = submission.timeLimit * realTimeFactor

    for testInd in subtaskData.orderIndSubtask:

        if subtaskData.subtasks[testInd].group:
            result[testInd] += "["
            print("[", end="", flush=True)
        elif len(subtaskData.orderIndSubtask) != 1:
            result[testInd] += "("
            print("(", end="", flush=True)

        correct = 0
        percentSumScore = 0.0
        isSkiped = False
        isPartial = False

        # Check if it prerequisite when it it contest
        if (submission.contestId) and subtaskData.subtasks[testInd].require:
            for req in subtaskData.subtasks[testInd].require:
                if not isPass[req]:
                    isSkiped = True

            if isSkiped:
                allCrt = len(subtaskData.subtasks[testInd].cases)
                correct = 0
                percentSumScore = 0.0
                print("S"*allCrt, end="", flush=True)
                result[testInd] += "S"*allCrt
                isPass[testInd] = False

        for testcaseNum in subtaskData.subtasks[testInd].cases:

            if isSkiped:
                break

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

            sumTime += testcaseResult.timeUse * 1000 // realTimeFactor
            if testcaseResult.memUse != -1:
                mxMem = max(mxMem or 0, testcaseResult.memUse)

            if testcaseResult.status == VerdictStatus.accept:
                correct += 1
            elif testcaseResult.status == VerdictStatus.partial:
                isPartial = True

            percentSumScore += testcaseResult.percent

            result[testInd] += verdictSymbol(testcaseResult.status)
            print(verdictsColorSymbol(testcaseResult.status), end="", flush=True)

            onUpdateRuningInCase(submission.id, testcaseNum)

        # calculate score here
        allCorrect = len(subtaskData.subtasks[testInd].cases)
        if subtaskData.subtasks[testInd].group:
            if correct != allCorrect:
                correct = 0
                percentSumScore = 0

        isPass[testInd] = (correct == allCorrect)

        realCorrect = correct
        if isPartial:
            realCorrect = percentSumScore

        score += realCorrect * \
            float(subtaskData.subtasks[testInd].score) / allCorrect
        mxScore += float(subtaskData.subtasks[testInd].score)

        if subtaskData.subtasks[testInd].group:
            result[testInd] += "]"
            print("]", end="", flush=True)
        elif len(subtaskData.orderIndSubtask) != 1:
            result[testInd] += ")"
            print(")", end="", flush=True)

    for res in result:
        if "!" in res:
            printFail(
                "JUDGE ERROR", f"There are some case that '{evaData.judgeType.value}' was explode during evaluate")
            return ResultDTO(submission.id,
                             "Judge Error", 0, 0, 0, f"It's the problem author's fault!\nGomennasai...\n\n\n{evaData.judgeType.value} was explode during evaluate")

    finalResult = "".join(result)
    finalScore = round(score * submission.maxScore / mxScore)

    return ResultDTO(submission.id,
                     finalResult, finalScore, sumTime, mxMem, None)
