from DTO.submission import submissionDTO
from handle import *
import subtask
from postgresql.dbQuery import  updateRunningInCase
import constants as const
from constants.osDotEnv import *
import config

import cmdManager as langCMD
from constants.Enums import *


def classicEvaluate(submission: submissionDTO, srcPath: str, isoPath, onUpdateRuningInCase):
    judgeType = getTypeJudge(submission.problemId)

    printHeader("GRADER", f"use {judgeType.value} Judge...")
    printHeader("GRADER", f"Runtime process:")

    if os.path.exists(f"./source/{submission.problemId}/subtask.tc"):
        subContent = fileRead(f"./source/{submission.problemId}/subtask.tc")
        printHeader("SUBTASK", f"Found custom subtask")
    else:
        subContent = submission.testcase
    mxCase, subtaskData = subtask.compile(subContent)

    if mxCase == -1:
        printFail("SUBTASK", f"Subtask error : {subtaskData}")
        return "Judge Error", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo...\n\n\n{subtaskData}",

    # Invalid number of testcase
    if mxCase <= 0:
        printFail("GRADER", "Invalid number of testcase.")
        return "Invalid nCase", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo..",
        

    print("\t-> Result: ", end="", flush=True)
    testList, testOption = subtaskData
    seqCase = subtask.getSeq(testOption)
    isPass = [False for i in range(len(seqCase) + 5)]
    result = ["" for i in range(len(seqCase) + 5)]
    score = 0
    mxScore = 0
    sumTime = 0
    mxMem = None

    for testInd in seqCase:
        
        if "group" in testOption[testInd] and testOption[testInd]["group"]:
            result[testInd] += "["
            print("[", end="", flush=True)
        elif len(seqCase) != 1:
            result[testInd] += "("
            print("(", end="", flush=True)

        correct = 0
        isSkiped = False

        # Check if it prerequisite when it it contest
        if (submission.contestId) and "require" in testOption[testInd]:
            allReq = []
            if type(testOption[testInd]["require"]) == type(69) and testOption[testInd]["require"] <= len(testList):
                allReq.append(testOption[testInd]["require"])
            elif type(testOption[testInd]["require"]) == type([]):
                for req in testOption[testInd]["require"]:
                    if type(req) == type(69) and req <= len(testList):
                        allReq.append(req)
            for req in allReq:
                if not isPass[req]:
                    isSkiped = True
            if isSkiped:
                allCrt = len(testList[testInd-1])
                correct = 0
                print("S"*allCrt, end="", flush=True)
                result[testInd] += "S"*allCrt
                isPass[testInd] = False

        for x in testList[testInd-1]:

            if isSkiped:
                break

            testTimeLimit = submission.timeLimit * \
                langCMD.get(submission.language, "timeFactor") * \
                float(osEnv.GRADER_TIME_FACTOR)

            t, elapse, memUse = execute(
                submission.userId,  # User ID
                submission.problemId,  # Problem ID
                x,  # Index of testcase
                testTimeLimit,  # Time limit
                (submission.memoryLimit) * 1024,  # Memory limit (in kb)
                submission.language,  # Language
                srcPath,
                isoPath
            )
            userOutputPath = "env/output.txt"

            probOutputPath = f"./source/{submission.problemId}/{x}.sol"

            sumTime += elapse * 1000
            if memUse != None:
                if mxMem == None:
                    mxMem = memUse
                else:
                    mxMem = max(mxMem, memUse)
            errCode = error(t)
            if not errCode:
                verdict = getVerdict(
                    submission.problemId, userOutputPath, probOutputPath, x, srcPath, judgeType)
                if verdict == "P":
                    correct += 1

            elif errCode == "TLE":
                verdict = "T"
            else:
                verdict = "X"
            result[testInd] += verdict
            print(verdict, end="", flush=True)
            onUpdateRuningInCase(submission.id, x)

        # calculate score here
        allCorrect = len(testList[testInd-1])
        if "group" in testOption[testInd] and testOption[testInd]["group"]:
            if correct != allCorrect:
                correct = 0

        isPass[testInd] = (correct == allCorrect)

        if "score" in testOption[testInd]:
            score += correct * \
                float(testOption[testInd]["score"]) / allCorrect
            mxScore += float(testOption[testInd]["score"])
        else:
            score += correct
            mxScore += allCorrect

        if "group" in testOption[testInd] and testOption[testInd]["group"]:
            result[testInd] += "]"
            print("]", end="", flush=True)
        elif len(seqCase) != 1:
            result[testInd] += ")"
            print(")", end="", flush=True)

    for testInd in seqCase:
        if "!" in result[testInd]:
            return "Judge Error", 0, 0, 0, f"It's the problem author's fault!\nGomennasai...\n\n\n{judgeType.value} was explode in test case {result.find('!') + 1}",

    finalResult = "".join(result)
    finalScore = score * submission.mxScore / mxScore
    sumTime //= langCMD.get(submission.language, "timeFactor")

    return finalResult, finalScore, sumTime, mxMem, None


def cfEvaluate(submission: submissionDTO, srcPath: str, isoPath, onUpdateRuningInCase):
    judgeType = getTypeJudge(submission.problemId)

    printHeader("Codeforces", f"Evaluate with Codeforces standard")
    printHeader("GRADER", f"use {judgeType.value} Judge...")
    printHeader("GRADER", f"Runtime process:")

    if os.path.exists(f"./source/{submission.problemId}/subtask.tc"):
        subContent = fileRead(f"./source/{submission.problemId}/subtask.tc")
        printHeader("SUBTASK", f"Found custom subtask (But don't use in codeforce)")
    else:
        subContent = submission.testcase
    mxCase, subtaskData = subtask.compile(subContent)

    if mxCase == -1:
        printFail("SUBTASK", f"Subtask error : {subtaskData}")
        return "Judge Error", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo...\n\n\n{subtaskData}",

    # Invalid number of testcase
    if mxCase <= 0:
        printFail("GRADER", "Invalid number of testcase.")
        return "Invalid nCase", 0, 0, 0, f"Subtask error!!\nIt's the problem author's fault!\nNoooooo..",

    print("\t-> Result: ", end="", flush=True)
    result = "Accepted"
    resultTime = 0
    resultMem = 0

    for x in range(1, mxCase+1):

        testTimeLimit = submission.timeLimit * \
            langCMD(submission.language, "timeFactor") * \
                float(osEnv.GRADER_TIME_FACTOR)

        t, elapse, memUse = execute(
            submission.userId,  # User ID
            submission.problemId,  # Problem ID
            x,  # Index of testcase
            testTimeLimit,  # Time limit
            (submission.memoryLimit) * 1024,  # Memory limit (in kb)
            submission.language,  # Language
            srcPath,
            isoPath
        )

        userOutputPath = "env/output.txt"
        probOutputPath = f"./source/{submission.problemId}/{x}.sol"

        resultTime = max(resultTime, elapse * 1000)
        resultMem = max(resultMem, memUse)
        errCode = error(t)
        verdict = ":)"
        if not errCode:
            verdict = getVerdict(
                submission.problemId, userOutputPath, probOutputPath, x, srcPath, judgeType)
        elif errCode == "TLE":  # T
            result = f"Time limit exceeded on pretest {x}"
        else:  # X
            result = f"Runtime error on pretest {x}"

        if result == "Accepted" and verdict != "P":  # - H Whatever
            result = f"Wrong answer on pretest {x}"

        if result != "Accepted":
            print(f"\n         ", result, flush=True)
            resultTime //= langCMD(submission.language, "timeFactor")
            return result, 0, resultTime, resultMem, None
        else:
            print('P', end="", flush=True)
            onUpdateRuningInCase(submission.id, x)

    resultTime //= langCMD(submission.language, "timeFactor")

    return result, submission.mxScore, resultTime, resultMem, None


def start(submission: submissionDTO, srcPath: str, isoPath, onUpdateRuningInCase):

    if submission.mode == "codeforces":
        return cfEvaluate(submission, srcPath, isoPath, onUpdateRuningInCase)
    else:
        return classicEvaluate(submission, srcPath, isoPath, onUpdateRuningInCase)
