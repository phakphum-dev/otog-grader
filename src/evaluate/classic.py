import os

from DTO.evaluate import EvaluateData
from DTO.result import ResultDTO
from handle import error
from checkType import *
import cmdManager as langCMD
from constants.osDotEnv import *
from constants.Enums import VerdictStatus
from constants.verdict import verdictSymbol, verdictsColorSymbol

from evaluate.verdict.main import excuteAndVerdict

from message import *
import subtask


def evaluate(evaData: EvaluateData, isoPath: str, onUpdateRuningInCase: str, subtaskData) -> ResultDTO:

    submission = evaData.submission

    printHeader("GRADER", f"use {evaData.judgeType.value} Judge...")
    printHeader("GRADER", f"Runtime process:")

    print("\t-> Result: ", end="", flush=True)
    testList, testOption = subtaskData
    seqCase = subtask.getSeq(testOption)
    isPass = [False for i in range(len(seqCase) + 5)]
    result = ["" for i in range(len(seqCase) + 5)]
    score = 0
    mxScore = 0
    sumTime = 0
    mxMem = None

    realTimeFactor = langCMD.get(
        submission.language, "timeFactor") * float(osEnv.GRADER_TIME_FACTOR)
    testTimeLimit = submission.timeLimit * realTimeFactor

    for testInd in seqCase:

        if "group" in testOption[testInd] and testOption[testInd]["group"]:
            result[testInd] += "["
            print("[", end="", flush=True)
        elif len(seqCase) != 1:
            result[testInd] += "("
            print("(", end="", flush=True)

        correct = 0
        percentSumScore = 0.0
        isSkiped = False
        isPartial = False

        # Check if it prerequisite when it it contest
        if (submission.contestId) and "require" in testOption[testInd]:
            allReq = []
            if isInt(testOption[testInd]["require"]) and testOption[testInd]["require"] <= len(testList):
                allReq.append(testOption[testInd]["require"])
            elif isList(testOption[testInd]["require"]):
                for req in testOption[testInd]["require"]:
                    if isInt(req) and req <= len(testList):
                        allReq.append(req)
            for req in allReq:
                if not isPass[req]:
                    isSkiped = True
            if isSkiped:
                allCrt = len(testList[testInd-1])
                correct = 0
                percentSumScore = 0.0
                print("S"*allCrt, end="", flush=True)
                result[testInd] += "S"*allCrt
                isPass[testInd] = False

        for testcaseNum in testList[testInd-1]:

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
        allCorrect = len(testList[testInd-1])
        if "group" in testOption[testInd] and testOption[testInd]["group"]:
            if correct != allCorrect:
                correct = 0
                percentSumScore = 0

        isPass[testInd] = (correct == allCorrect)

        realCorrect = correct
        if isPartial:
            realCorrect = percentSumScore

        if "score" in testOption[testInd]:
            score += realCorrect * \
                float(testOption[testInd]["score"]) / allCorrect
            mxScore += float(testOption[testInd]["score"])
        else:
            score += realCorrect
            mxScore += allCorrect

        if "group" in testOption[testInd] and testOption[testInd]["group"]:
            result[testInd] += "]"
            print("]", end="", flush=True)
        elif len(seqCase) != 1:
            result[testInd] += ")"
            print(")", end="", flush=True)

    for testInd in seqCase:
        if "!" in result[testInd]:
            return ResultDTO(submission.id,
                             "Judge Error", 0, 0, 0, f"It's the problem author's fault!\nGomennasai...\n\n\n{evaData.judgeType.value} was explode in test case {result.find('!') + 1}")

    finalResult = "".join(result)
    finalScore = int(score * submission.maxScore / mxScore)

    return ResultDTO(submission.id,
                     finalResult, finalScore, sumTime, mxMem, None)
