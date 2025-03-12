import judge
from postgresql.dbQuery import DBConnect, DBDisconnect, getQueue, getQueueModBalace, testDBConnection, updateResult, updateRunningInCase, updateContestScore
from handle import testEnv
from message import *
import time
from DTO.submission import SubmissionDTO
from constants.osDotEnv import *


def main():

    testEnv()

    testDBConnection()
    printBlod("GRADER", "Grader started.")

    while True:
        DBConnect()
        nGrader, thisGrader = int(osEnv.LOAD_BALANCE_N_GRADER), int(
            osEnv.LOAD_BALANCE_THIS_GRADER)
        queue = getQueueModBalace(nGrader, thisGrader)
        getQueue() # why do we need another getQueue btw
        if not queue:
            DBDisconnect()
            time.sleep(1)
            continue
        problemPath = f"./source/{queue.problemId}"
        subDTO = SubmissionDTO(
            id=queue.id,
            userId=queue.userId,
            problemId=queue.problemId,
            problemPath=problemPath,
            contestId=queue.contestId,
            sourceCode=queue.sourceCode,
            language=queue.language,
            maxScore=queue.maxScore,
            timeLimit=queue.timeLimit,
            memoryLimit=queue.memoryLimit,
            testcase=queue.case,
            mode="classic"
        )
        judge.startJudge(subDTO, updateResult, updateRunningInCase, updateContestScore)
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
