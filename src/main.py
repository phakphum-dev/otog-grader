from pathlib import Path
import time
from datetime import datetime
import tabulate

import subtask
from message import *
from postgresql.dbQuery import DBConnect, DBDisconnect, getQueue, testDBConnection, updateResult, updateRunningInCase
from handle import *
from DTO.submission import submissionDTO
import evaluate


def startJudge(queueData, isTest: bool = False):

    if isTest:
        def updateResult(subName, result, score, timeLen, comment):
            print(f"\n\n-------------End of submit {subName}-------------")
            print(f"result : {result}")
            print(f"score : {score}")
            print(f"timeLen : {timeLen}")
            print(f"comment : {comment}")
            print(f"-----------------------------------------------")

    # If there is new payload
    submission = submissionDTO(queueData)
    printOKCyan("GRADER", "Receive New Submission.")
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
        printFail("GRADER", "Number of testcase does not specified.")
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
        printFail("GRADER", "No testcase. Aborted.")
        updateResult(
            submission.id,
            "No Testcase",
            0,
            0,
            "Admins have not yet upload the testcases. Go ahead and flame them.",
        )
        return

    printHeader("GRADER", "Compiling process...")

    try:
        sourceCode = submission.sourceCode.decode("UTF-8")
    except:
        printFail("GRADER", "Cannot decode received source string. Aborted.")
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
        printOKCyan("GRADER", "Compile error.")
        try:
            errmsg = fileRead("env/error.txt") or None
        except:
            errmsg = "Someting went wrong."

        if errmsg != None:
            errmsg = errMsgHandle(errmsg)

        updateResult(submission.id, err, 0, 0, errmsg)
        return

    result, finalScore, sumTime, comment = evaluate.start(
        submission, srcCodePath, isTest)
    updateResult(
        submission.id,
        result,
        finalScore,
        sumTime,
        comment,
    )

    if not err:
        print(f"\n\t-> Time used: {int(sumTime)} ms.")


def main():

    testEnv()

    testDBConnection()
    printBlod("GRADER", "Grader started.")

    while True:
        DBConnect()
        queue = getQueue()
        if not queue:
            DBDisconnect()
            time.sleep(1)
            continue
        startJudge(queue)
        printOKCyan(
            "GRADER", "Grading session completed.\n\t-> Waiting for new submission.")
        DBDisconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(" Keyboard Interrupt Detected.\n")
    except Exception as e:
        print("Exception : "+str(e)+"\n")
