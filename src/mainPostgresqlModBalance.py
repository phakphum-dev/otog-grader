import judge
from postgresql.dbQuery import DBConnect, DBDisconnect, getQueue, getQueueModBalace, testDBConnection, updateResult, updateRunningInCase
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
        getQueue()
        if not queue:
            DBDisconnect()
            time.sleep(1)
            continue
        subDTO = SubmissionDTO(
            id=queue[0],
            userId=queue[1],
            problemId=queue[2],
            contestId=queue[8],
            sourceCode=queue[9],
            language=queue[10],
            maxScore=queue[16],
            timeLimit=queue[17],
            memoryLimit=queue[18],
            testcase=queue[21],
            mode="classic"
        )
        judge.startJudge(subDTO, updateResult, updateRunningInCase)
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
