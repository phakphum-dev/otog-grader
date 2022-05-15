import os

from DTO.evaluate import EvaluateData
from DTO.result import ResultDTO
from constants.Enums import VerdictStatus
from handle import error
from constants.osDotEnv import *
import cmdManager as langCMD
from evaluate.verdict.main import excuteAndVerdict
from constants.verdict import  verdictsColorSymbol

from message import *

def evaluate(evaData: EvaluateData, isoPath: str, onUpdateRuningInCase: str, mxCase:int) -> ResultDTO :
    
    submission = evaData.submission
    
    printHeader("Codeforces", f"Evaluate with Codeforces standard")
    printHeader("GRADER", f"use {evaData.judgeType.value} Judge...")
    printHeader("GRADER", f"Runtime process:")

    print("\t-> Result: ", end="", flush=True)
    result = "Accepted"
    resultTime = 0
    resultMem = 0

    for x in range(1, mxCase+1):

        testTimeLimit = submission.timeLimit * \
            langCMD.get(submission.language, "timeFactor") * \
            float(osEnv.GRADER_TIME_FACTOR)

        testcaseResult = excuteAndVerdict(
                submission.problemId,
                x,
                testTimeLimit,
                (submission.memoryLimit) * 1024,
                submission.language,
                evaData.srcPath,
                isoPath,
                evaData.judgeType
            )

        resultTime = max(resultTime, testcaseResult.timeUse * 1000)
        resultMem = max(resultMem, testcaseResult.memUse)
        
        if testcaseResult.status != VerdictStatus.accept:
            if testcaseResult.status == VerdictStatus.partial:
                result = f"Partial correct on pretest {x}"
            elif testcaseResult.status == VerdictStatus.reject:
                result = f"Wrong answer on pretest {x}"
            elif testcaseResult.status == VerdictStatus.timeExceed:
                result = f"Time limit exceeded on pretest {x}"
            elif testcaseResult.status == VerdictStatus.runtimeErr:
                result = f"Runtime error on pretest {x}"
            elif testcaseResult.status == VerdictStatus.err:
                result = f"Judge error on pretest {x}"
            
            print(f"\n         ", result, flush=True)
            resultTime //= langCMD.get(submission.language, "timeFactor")

            return ResultDTO(submission.id, result, 0, resultTime, resultMem, None)

        print(verdictsColorSymbol(testcaseResult.status), end="", flush=True)
        onUpdateRuningInCase(submission.id, x)


    #? mean accept every testcase
    resultTime //= langCMD.get(submission.language, "timeFactor")

    return ResultDTO(submission.id, result, submission.maxScore, resultTime, resultMem, None)