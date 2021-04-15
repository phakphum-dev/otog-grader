from pathlib import Path
import time
import tabulate

from constants import bcolors, langarr
from database import getQueue, updateRunningInCase, updateResult, closeConnection, testConnection
from handle import create, execute, error, cmpfunc, createSourceCode, file_read
from DTO import submissionDTO


def main():
    try:
        testConnection()
    except:
        print(bcolors.FAIL + 'Mysql: Connection Fail.' + bcolors.RESET)
        exit(1)
    print(bcolors.BOLD +
          "--------Grader started---------" +
          bcolors.RESET)
    while True:
        queue = getQueue()
        if(queue != None):
            s = submissionDTO(queue)
            result = ''
            count = 0
            sumTime = 0
            print(bcolors.OKCYAN +
                  "Receive New Submission." +
                  bcolors.RESET
                  )
            print(tabulate.tabulate([
                ['id', s.id],
                ['userId', s.userId],
                ['problemId', s.problemId],
                ['language', s.language],
                ['case', s.testcase],
            ],
                headers=['info', 'value'],
                tablefmt='orgtbl'
            ))
            print(bcolors.HEADER +
                  "------Compilation Process------" +
                  bcolors.RESET)
            try:
            	sourceCode = s.sourceCode.decode('UTF-8')
            except:
            	err = "Compilation Error"
            createSourceCode(sourceCode, s.language)
            err = create(s.userId, s.language)
            if s.testcase != None:
                testcase = [int(e) for e in s.testcase.split()]
            if s.contestId == None:
                testcase = testcase[-1:]
            if not Path(f'./source/{s.problemId}').is_dir():
                print(bcolors.FAIL + 'No testcases.' + bcolors.RESET)
                err = 'No testcases.'
            if(err == None):
                print(bcolors.HEADER +
                      "--------Runtime Process--------" +
                      bcolors.RESET)
                print("Result: ", end='', flush=True)
                for sub in testcase:
                    for x in range(sub):
                        t, timediff = execute(s.userId, s.problemId, x+1,
                                              s.timeLimit, (s.memoryLimit)*1024, s.language)
                        userOutput = "env/output.txt"
                        probOutput = f'''source/{s.problemId}/{x+1}.sol'''
                        sumTime += (timediff*1000)
                        errCode = error(t)
                        if(errCode == None and t == 0):
                            if(cmpfunc(userOutput, probOutput)):
                                o = 'P'
                                count += 1
                            else:
                                o = '-'
                        elif(errCode == 'TLE'):
                            o = 'T'
                        else:
                            o = 'X'
                        result += o
                        print(o, end='', flush=True)
                        updateRunningInCase(s.id, x)
            else:
                result = err
            try:
                errmsg = file_read("env/error.txt")
                errmsg = errmsg if errmsg else None
            except:
                errmsg = "Something wrong."
            score = (count / int(testcase[-1])) * s.mxScore
            updateResult(s.id, result, score, s.mxScore, sumTime, errmsg)
            if not err:
                print(f'''\ntimeUsed: {int(sumTime)}''')
            print(bcolors.HEADER +
                  '-------Grading Complete--------' +
                  bcolors.RESET
                  )
            print("Wait For New Submission...")
        time.sleep(1)


if __name__ == "__main__":
    main()
    closeConnection()
