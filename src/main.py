from pathlib import Path
import time
from datetime import datetime
import tabulate
import subtask

from constants.colors import colors
from database.dbQuery import DBConnect, DBDisconnect, getQueue, testDBConnection, updateResult, updateRunningInCase
from handle import *
from DTO.submission import submissionDTO

PYTIMEFACTOR = 25


def startJudge(queueData):
    # If there is new payload
    submission = submissionDTO(queueData)
    result = ""
    count = 0
    sumTime = 0
    print(f"[ {colors.OKCYAN}GRADER{colors.RESET} ] Receive New Submission.")
    print(f"[ {datetime.now().strftime('%d/%m/%Y - %H:%M:%S')} ]")
    print(
        tabulate.tabulate(
            [
                ["id", submission.id],
                ["userId", submission.userId],
                ["problemId", submission.problemId],
                ["language", submission.language],
                ["case", submission.testcase],
            ],
            headers=["info", "value"],
            tablefmt="orgtbl",
        )
    )

    # If does not specify number of testcase
    if not submission.testcase:
        print(
            f"[ {colors.FAIL}GRADER{colors.RESET} ] Number of testcase does not specified."
        )
        updateResult(
            submission.id,
            "No nCase",
            0,
            0,
            "Number of testcase does not specified. Flame admins, kiddos. :(",
        )
        return

    # Check if testcases actually exist
    if not Path(f"./source/{submission.problemId}").is_dir():
        print(f"[ {colors.FAIL}GRADER{colors.RESET} ] No testcase. Aborted.")
        updateResult(
            submission.id,
            "No Testcase",
            0,
            0,
            "Admins have not yet upload the testcases. Go ahead and flame them.",
        )
        return

    print(f"[ {colors.HEADER}GRADER{colors.RESET} ] Compiling process...")

    try:
        sourceCode = submission.sourceCode.decode("UTF-8")
    except:
        print(
            f"[ {colors.FAIL}GRADER{colors.RESET} ] Cannot decode recieved source string. Aborted."
        )
        updateResult(
            submission.id,
            "Undecodable",
            0,
            0,
            "Cannot decode your submitted code. Check your submission.",
        )
        return

    prepareEnv(submission.problemId)

    # Write source string to file
    srcCodePath = createSourceCode(sourceCode, submission.language)

    # Compile
    err = create(submission.userId, submission.language,
                 srcCodePath, submission.problemId)

    # If compile error
    if err:
        print(f"[ {colors.OKCYAN}GRADER{colors.RESET} ] Compile error.")
        try:
            errmsg = fileRead("env/error.txt") or None
        except:
            errmsg = "Someting went wrong."

        if errmsg != None:
            errmsg = errMsgHandle(errmsg)

        updateResult(submission.id, err, 0, 0, errmsg)
        return

    # Split testcase into subtasks if available
    testcase = int(submission.testcase)

    judgeType = getTypeJudge(submission.problemId)

    print(f"[ {colors.HEADER}GRADER{colors.RESET} ] use {judgeType} Judge...")
    print(f"[ {colors.HEADER}GRADER{colors.RESET} ] Runtime process:")

    if os.path.exists(f"./source/{submission.problemId}/subtask.tc"):
        subContent = fileRead(f"./source/{submission.problemId}/subtask.tc")
        mxCase, bigSubdata = subtask.compile(subContent)
        if mxCase == -1:
            print(
                f"[ {colors.FAIL}SUBTASK{colors.RESET} ] Subtask error : {bigSubdata}")
            updateResult(
                submission.id,
                "Judge Error",
                0,
                0,
                f"Subtask error!!\nIt's the problem author's fault!\nNoooooo...\n\n\n{bigSubdata}",
            )
            return
        elif testcase != mxCase:
            print(
                f"[ {colors.FAIL}SUBTASK{colors.RESET} ] Expect {mxCase} cases but got {testcase}")
            updateResult(
                submission.id,
                "Judge Error",
                0,
                0,
                f"Subtask error!!\nIt's the problem author's fault!\nNoooooo...\n\n\nExpect {mxCase} cases but got {testcase}",
            )
            return
        else:
            print(f"[ {colors.HEADER}SUBTASK{colors.RESET} ] use custom subtask")
    else:
        mxCase, bigSubdata = testcase, ([[i for i in range(
            1, testcase + 1)]], {1: {"group": False, "score": testcase}})

    print("\t-> Result: ", end="", flush=True)
    testcases, subData = bigSubdata
    seqCase = subtask.getSeq(subData)
    isPass = [False for i in range(len(seqCase) + 5)]
    score = 0
    mxScore = 0
    result = ""

    for testInd in seqCase:
        if len(seqCase) != 1:
            if "group" in subData[testInd] and subData[testInd]["group"]:
                result += "["
                print("[", end="", flush=True)
            else:
                result += "("
                print("(", end="", flush=True)
        correct = 0
        isSkiped = False
        # Check if it prerequisite when it it contest
        if submission.contestId and "require" in subData[testInd]:
            allReq = []
            if type(subData[testInd]["require"]) == type(69) and subData[testInd]["require"] <= len(testcases):
                allReq.append(subData[testInd]["require"])
            elif type(subData[testInd]["require"]) == type([]):
                for req in subData[testInd]["require"]:
                    if type(req) == type(69) and req <= len(testcases):
                        allReq.append(req)
            for req in allReq:
                if not isPass[req]:
                    isSkiped = True
            if isSkiped:
                allCrt = len(testcases[testInd-1])
                correct = 0
                print("S"*allCrt, end="", flush=True)
                result += "S"*allCrt
                isPass[testInd] = False

        for x in testcases[testInd-1]:

            if isSkiped:
                break

            t, elapse = execute(
                submission.userId,  # User ID
                submission.problemId,  # Problem ID
                x,  # Index of testcase
                submission.timeLimit
                * (
                    PYTIMEFACTOR if submission.language == "python" else 1
                ),  # Time limit
                (submission.memoryLimit) * 1024,  # Memory limit (in kb)
                submission.language,  # Language
                srcCodePath
            )

            userOutputPath = "env/output.txt"
            probOutputPath = f"./source/{submission.problemId}/{x}.sol"

            sumTime += elapse * 1000
            errCode = error(t)
            if not errCode:
                verdict = getVerdict(
                    submission.problemId, userOutputPath, probOutputPath, x, srcCodePath, judgeType)
                if verdict == "P":
                    correct += 1

            elif errCode == "TLE":
                verdict = "T"
            else:
                verdict = "X"
            result += verdict
            print(verdict, end="", flush=True)
            updateRunningInCase(submission.id, x)

        # calculate score here
        allCorrect = len(testcases[testInd-1])
        if "group" in subData[testInd] and subData[testInd]["group"]:
            if correct != allCorrect:
                correct = 0

        isPass[testInd] = (correct == allCorrect)

        if "score" in subData[testInd]:
            score += correct * \
                float(subData[testInd]["score"]) / allCorrect
            mxScore += float(subData[testInd]["score"])
        else:
            score += correct
            mxScore += allCorrect

        if len(seqCase) != 1:
            if "group" in subData[testInd] and subData[testInd]["group"]:
                result += "]"
                print("]", end="", flush=True)
            else:
                result += ")"
                print(")", end="", flush=True)

    if "!" in result:
        updateResult(
            submission.id,
            "Judge Error",
            0,
            0,
            f"It's the problem author's fault!\nGomennasai...\n\n\n{judgeType} was explode in test case {result.find('!') + 1}",
        )
        return

    finalScore = score * submission.mxScore / mxScore

    errmsg = fileRead("env/error.txt") or None
    updateResult(
        submission.id,
        result,
        finalScore,
        sumTime // ((PYTIMEFACTOR if submission.language == "python" else 1)),
        None,
    )

    if not err:
        print(f"\n\t-> Time used: {int(sumTime)} ms.")


def main():

    testEnv()

    testDBConnection()

    print(f"[ { colors.BOLD}GRADER{colors.RESET} ] Grader started.")

    while True:
        DBConnect()
        queue = getQueue()
        if not queue:
            DBDisconnect()
            time.sleep(1)
            continue
        startJudge(queue)
        print(f"[ {colors.OKCYAN}GRADER{colors.RESET} ] Grading session completed.\n\t-> Waiting for new submission.")
        DBDisconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(" Keyboard Interrupt Detected.\n")
    except Exception as e:
        print("Exception : "+str(e)+"\n")
