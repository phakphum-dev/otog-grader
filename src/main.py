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
from constants import Enums


def startJudge(queueData, isTest: bool = False):
    global updateResult
    if isTest:
        def updateResult(subName, result, score, timeLen, memUse, comment):
            print(f"\n\n-------------End of submit {subName}-------------")
            print(f"result : {result}")
            print(f"score : {score}")
            print(f"timeLen : {timeLen}")
            print(f"memUse : {memUse}")
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
            0,
            "Admins have not yet upload the testcases. Go ahead and flame them.",
        )
        return
    
    #? Check is .in are ready to use
    missingIn = getMissingSeqNumberFile(f"./source/{submission.problemId}","in",int(submission.testcase))
    if missingIn:
        printFail("TESTCASE", f"Testcase {missingIn[0]}.in is missing")
        updateResult(
            submission.id,
            "Input missing",
            0,
            0,
            0,
            "Admins have not yet upload the testcases. Go ahead and flame them.",
        )
        return
    
    missingSol = getMissingSeqNumberFile(f"./source/{submission.problemId}","sol",int(submission.testcase))
    #? to check .sol It depend on type of judge
    judgeType = getTypeJudge(submission.problemId)
    if judgeType == Enums.JudgeType.standard:
        #? if it standard, It must have all .sol file
        if missingSol:
            printFail("TESTCASE", f"Testcase {missingSol[0]}.sol is missing")
            updateResult(
                submission.id,
                "Solution missing",
                0,
                0,
                0,
                "Admins have not yet upload the testcases. Go ahead and flame them.",
            )
            return
    else:
        #? otherwise, just warn.
        for e in missingSol:
            printWarning("TESTCASE", f"Testcase {e}.sol is missing")



    printHeader("GRADER", "Compiling process...")

    # try:
    #     sourceCode = submission.sourceCode.decode("UTF-8")
    # except:
    #     printFail("GRADER", "Cannot decode received source string. Aborted.")
    #     updateResult(
    #         submission.id,
    #         "Undecodable",
    #         0,
    #         0,
    #         69,
    #         "Cannot decode your submitted code. Check your submission.",
    #     )
    #     return

    #? check and init isolate
    isolateEnvPath = None #! None means didn't use isolate
    if config.getAsBool("grader", "use_isolate"):
        isolateEnvPath = initIsolate()
    

    prepareEnv(submission.problemId, isolateEnvPath)

    # Write source string to file
    srcCodePath = createSourceCode(submission.sourceCode, submission.language, isolateEnvPath)

    # Compile
    err = create(submission.userId, submission.language,
                 srcCodePath, submission.problemId, isolateEnvPath)

    # If compile error
    if err == "Compilation Error":
        printOKCyan("GRADER", "Compile error.")
        try:
            if isolateEnvPath != None:
                errmsg = fileRead(f"{isolateEnvPath}/error.txt") or None
            else:
                errmsg = fileRead("env/error.txt") or None

        except:
            errmsg = "Someting went wrong."

        if errmsg:
            errmsg = errMsgHandle(errmsg)
        else:
            errmsg = "Someting went wrong.\nContact admin immediately :( !!"
            

        updateResult(submission.id, err, 0, 0, 0, errmsg)
        return
    elif err == "Compilation TLE":
        printWarning("GRADER", "Compile Time Limit Exceeded.")
        updateResult(submission.id, "Compilation Error", 0, 0, 0, "Compilation Time Limit Exceeded")
        return

    result, finalScore, sumTime, resMem, comment = evaluate.start(
        submission, srcCodePath, isTest, isolateEnvPath)
    updateResult(
        submission.id,
        result,
        finalScore,
        sumTime,
        resMem,
        comment,
    )

    if not err:
        print(f"\n\t-> Time used: {int(sumTime)} ms.")
        print(f"\t-> Mem  used: {int(resMem or -1)} kb??")


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
