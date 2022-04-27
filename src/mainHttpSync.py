import judge
from httpSync.httpQuery import getTask, updateResult, updateRunningInCase
from handle import testEnv
from message import *
import time
from DTO.submission import SubmissionDTO


def main():

    testEnv()

    printBlod("GRADER", "Grader started.")

    while True:
        task = getTask()
        if not task:
            time.sleep(1)
            continue
        subDTO = SubmissionDTO(
            id=task['id'],
            userId=task['userId'],
            problemId=task['problemId'],
            contestId=task['contestId'],
            sourceCode=task['sourceCode'],
            language=task['language'],
            maxScore=task['maxScore'],
            timeLimit=task['timeLimit'],
            memoryLimit=task['memoryLimit'],
            testcase=task['testcase'],
            mode=task['mode']
        )
        judge.startJudge(subDTO, updateResult, updateRunningInCase)
        printOKCyan(
            "GRADER", "Grading session completed.\n\t-> Waiting for new submission.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(" Keyboard Interrupt Detected.\n")
    except Exception as e:
        print("Exception : "+str(e)+"\n")
