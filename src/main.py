from pathlib import Path
import time
from datetime import datetime
import tabulate

from constants import bcolors, langarr
from database import (
    getQueue,
    updateRunningInCase,
    updateResult,
    closeConnection,
    testConnection,
)
from handle import *
from DTO import submissionDTO

PYTIMEFACTOR = 25


def main():
    try:
        testConnection()
    except:
        print(f"[ {bcolors.FAIL}MYSQL{bcolors.RESET} ] Connection failed.")
        exit(1)
    print(f"[ { bcolors.BOLD}GRADER{bcolors.RESET} ] Grader started.")

    while True:
        queue = getQueue()
        if not queue:
            time.sleep(1)
            continue

        # If there is new payload
        submission = submissionDTO(queue)
        result = ""
        count = 0
        sumTime = 0
        print(f"[ {bcolors.OKCYAN}GRADER{bcolors.RESET} ] Receive New Submission.")
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
                f"[ {bcolors.FAIL}GRADER{bcolors.RESET} ] Number of testcase does not specified."
            )
            updateResult(
                submission.id,
                "No nCase",
                0,
                0,
                "Number of testcase does not specified. Flame admins, kiddos. :(",
            )
            continue

        # Check if testcases actually exist
        if not Path(f"./source/{submission.problemId}").is_dir():
            print(f"[ {bcolors.FAIL}GRADER{bcolors.RESET} ] No testcase. Aborted.")
            updateResult(
                submission.id,
                "No Testcase",
                0,
                0,
                "Admins have not yet upload the testcases. Go ahead and flame them.",
            )
            continue

        print(f"[ {bcolors.HEADER}GRADER{bcolors.RESET} ] Compiling process...")

        try:
            sourceCode = submission.sourceCode.decode("UTF-8")
        except:
            print(
                f"[ {bcolors.FAIL}GRADER{bcolors.RESET} ] Cannot decode recieved source string. Aborted."
            )
            updateResult(
                submission.id,
                "Undecodable",
                0,
                0,
                "Cannot decode your submitted code. Check your submission.",
            )
            continue

        prepareEnv(submission.problemId)

        # Write source string to file
        srcCodePath = createSourceCode(sourceCode, submission.language)

        # Compile
        err = create(submission.userId, submission.language,
                     srcCodePath, submission.problemId)

        # If compile error
        if err:
            print(f"[ {bcolors.OKCYAN}GRADER{bcolors.RESET} ] Compile error.")
            try:
                errmsg = fileRead("env/error.txt") or None
            except:
                errmsg = "Someting went wrong."

            if errmsg != None:
                errmsg = errMsgHandle(errmsg)

            updateResult(submission.id, err, 0, 0, errmsg)
            continue

        # Split testcase into subtasks if available
        testcase = [int(e) for e in submission.testcase.split()]

        # For contest mode
        if not submission.contestId:
            testcase = testcase[-1:]

        judgeType = getTypeJudge(submission.problemId)

        print(f"[ {bcolors.HEADER}GRADER{bcolors.RESET} ] use {judgeType} Judge...")
        print(f"[ {bcolors.HEADER}GRADER{bcolors.RESET} ] Runtime process:")
        print("\t-> Result: ", end="", flush=True)
        for sub in testcase:
            for x in range(sub):
                t, elapse = execute(
                    submission.userId,  # User ID
                    submission.problemId,  # Problem ID
                    x + 1,  # Index of testcase
                    submission.timeLimit
                    * (
                        PYTIMEFACTOR if submission.language == "python" else 1
                    ),  # Time limit
                    (submission.memoryLimit) * 1024,  # Memory limit (in kb)
                    submission.language,  # Language
                    srcCodePath
                )

                userOutputPath = "env/output.txt"
                probOutputPath = f"./source/{submission.problemId}/{x+1}.sol"

                sumTime += elapse * 1000
                errCode = error(t)
                if not errCode:
                    verdict = getVerdict(
                        submission.problemId, userOutputPath, probOutputPath, x+1, srcCodePath, judgeType)
                    if verdict == "P":
                        count += 1

                elif errCode == "TLE":
                    verdict = "T"
                else:
                    verdict = "X"
                result += verdict
                print(verdict, end="", flush=True)
                updateRunningInCase(submission.id, x)

        score = (count / int(testcase[-1])) * submission.mxScore

        if "!" in result:  # If it Judge Error
            updateResult(
                submission.id,
                "Judge Error",
                0,
                0,
                f"It's the problem author's fault!\nGomennasai...\n\n\n{judgeType} was explode in test case {result.find('!') + 1}",
            )
            continue

        errmsg = fileRead("env/error.txt") or None
        updateResult(
            submission.id,
            result,
            score,
            sumTime // ((PYTIMEFACTOR if submission.language == "python" else 1)),
            errmsg,
        )

        if not err:
            print(f"\n\t-> Time used: {int(sumTime)} ms.")

        print(f"[ {bcolors.OKCYAN}GRADER{bcolors.RESET} ] Grading session completed.\n\t-> Waiting for new submission.")


if __name__ == "__main__":
    main()
    closeConnection()
