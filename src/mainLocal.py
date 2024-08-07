import configparser
import time
import os, stat


from DTO.submission import SubmissionDTO
from DTO.result import ResultDTO
from message import *
from handle import *
import judge

reportTextLog = ""


def updateResult(result: ResultDTO):
    global reportTextLog
    print(f"\n\n-------------End of submit {result.id}-------------")
    print(f"result : {result.result}")
    print(f"score : {result.score}")
    print(f"timeLen : {result.sumTime}")
    print(f"memUse  : {result.memUse}")
    print(f"comment : {result.errmsg}")
    print(f"-----------------------------------------------")
    reportTextLog += f"""**Result** : `{result.result}`

**Score** : `{result.score}`

**TimeLen** : `{result.sumTime}s`

**MemUse** : `{result.memUse}kb`

**Comment**

```
{result.errmsg}
```


"""


def runCase(id, case):
    pass


fileExtension = {
    "c": ["c", "i"],
    "cpp": ["cpp", "cc", "cxx", "c++", "hpp", "hh", "hxx", "h++", "h", "ii"],
    "python": ["py", "rpy", "pyw", "cpy", "gyp", "gypi", "pyi", "ipy"]
}


def testSubmit(crt, subName, proId, srcCode: str, testcase, lang="cpp", mem=256, timeLim=10):
    
    nUser = crt * 100 + 69
    # If there is new payload
    problemPath = f"./source/{proId}"
    submission = SubmissionDTO(
        nUser,
        nUser,
        proId,
        problemPath,
        69,
        srcCode, lang, 100,
        timeLim * 1000, mem, testcase, "classic"
    )
    judge.startJudge(submission, updateResult, runCase)

def prepareTestEnvironment():
    #? check is ./testSpace/logs exist or not
    if not os.path.exists("./testSpace/logs"): os.mkdir("./testSpace/logs")

    if not os.path.exists("./testSpace/codes"): 
        os.mkdir("./testSpace/codes")
        os.chmod("./testSpace/codes", 0o0777)
        printWarning("CODE TESTs", "directory codes justs created, you can add codes to test on grader in pattern like this <problemId>/<code.c>")

if __name__ == "__main__":
    
    testEnv() #? in main grader
    prepareTestEnvironment()

    testCaseConfig = configparser.ConfigParser()
    testCaseConfig.read("./testSpace/testCodeDB.ini")

    thisTime = time.localtime(time.time())
    logFileName = f"{thisTime.tm_year}{thisTime.tm_mon:02d}{thisTime.tm_mday:02d}-{thisTime.tm_hour:02d}{thisTime.tm_min:02d}{thisTime.tm_sec:02d}.md"
    thisTimeInStr = f"{thisTime.tm_mday} {('?','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[thisTime.tm_mon]} {thisTime.tm_year} {thisTime.tm_hour:02d}\:{thisTime.tm_min:02d}\:{thisTime.tm_sec:02d}"
    with open(f"./testSpace/logs/{logFileName} waiting", "w") as f:
        f.write(f"# Report {thisTimeInStr}\n\n_missing_")
    reportTextLog = f"# Report {thisTimeInStr}\n\n"

    def isInt(somStr: str) -> bool:
        try:
            int(somStr)
        except:
            return False
        return True

    def getLang(ex):
        for lang in fileExtension:
            for e in fileExtension[lang]:
                if ex == e:
                    return lang

        return "?"

    allPTestFolder = [x for x in os.listdir(
        f"./testSpace/codes/") if os.path.isdir(f"./testSpace/codes/{x}") and isInt(x)]

    crt = 0

    for testP in allPTestFolder:
        printHeader("PROBLEM", f"{testP}\n\n\n")
        reportTextLog += f"## Problem {testP}\n\n"

        if testP not in testCaseConfig:
            print(f"No config in {testP}.... skiping!")
            print(f"TIP : you can config in testSpace/testCodeDB.ini")
            reportTextLog += f"No config in {testP}.... skiping!\n_you can config in `testSpace/testCodeDB.ini`_\n\n"
            continue

        if "TestCase" not in testCaseConfig[testP]:
            print(
                f"Please specify the number of test case ({testP}) in testCodeDB.ini")
            reportTextLog += f"_Please specify the number of test case ({testP}) in testCodeDB.ini_\n\n"
            continue

        if "Memory" in testCaseConfig[testP]:
            configMem = int(testCaseConfig[testP]["Memory"])
        else:
            configMem = 256

        if "Time" in testCaseConfig[testP]:
            configTime = int(testCaseConfig[testP]["Time"])
        else:
            configTime = 10

        srcFiles = [x for x in os.listdir(
            f"./testSpace/codes/{testP}") if os.path.isfile(f"./testSpace/codes/{testP}/{x}") and (getLang(x[x.find(".")+1:].strip()) != "?")]

        for sFile in srcFiles:
            print("\n\n>>", end="")
            printOKBlue("TESTING", f"{sFile}...\n")

            codo = fileRead(f"./testSpace/codes/{testP}/{sFile}")
            lang = getLang(sFile[sFile.find(".")+1:].strip())

            reportTextLog += f"### File : {sFile}\n\n```{lang}\n{codo}\n```\n\n"

            testSubmit(crt, sFile, int(
                testP), codo, testCaseConfig[testP]["TestCase"], lang, configMem, configTime)

            crt += 1

            reportTextLog += f"---\n\n"

    os.remove(f"./testSpace/logs/{logFileName} waiting")
    if reportTextLog == f"# Report {thisTimeInStr}\n\n":
        with open(f"./testSpace/logs/{logFileName}", "w") as f:
            f.write(reportTextLog + "_but nobody came_")
    else:
        with open(f"./testSpace/logs/{logFileName}", "w") as f:
            f.write(reportTextLog)
