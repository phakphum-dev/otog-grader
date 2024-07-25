import configparser
import time
import os, stat
from os.path import isfile, isdir
from os.path import join as joinPath

from DTO.submission import SubmissionDTO
from DTO.result import ResultDTO
from message import *
from handle import *
import judge

lastResult = None
def updateResult(result: ResultDTO):
    global lastResult
    lastResult = result

def runCase(id, case):
    pass

fileExtension = {
    "c": ["c", "i"],
    "cpp": ["cpp", "cc", "cxx", "c++", "hpp", "hh", "hxx", "h++", "h", "ii"],
    "python": ["py", "rpy", "pyw", "cpy", "gyp", "gypi", "pyi", "ipy"]
}

class FailedTestDTO:
    def __init__(self, problem, file, message, ignore):
        self.problem = problem
        self.file = file
        self.message = message
        self.ignore = ignore


def testSubmit(crt, problemPath, proId, srcCode: str, testcase, mode, lang="cpp", mem=256, timeLim=10):
    
    nUser = crt * 100 + 69
    # If there is new payload
    submission = SubmissionDTO(
        nUser,
        nUser,
        proId,
        problemPath,
        69,
        srcCode, lang, 100,
        timeLim * 1000, mem, testcase, mode
    )
    judge.startJudge(submission, updateResult, runCase)

def printTest(header, text):
    bigPrint(header, text, colors.TEST_HEADER)

def printPass(header, text):
    bigPrint(header, text, colors.OKGREEN, True)

def printFail(header, text):
    bigPrint(header, text, colors.FAIL, True)

def printWarning(header, text):
    bigPrint(header, text, colors.WARNING, True)

def isInt(somStr: str) -> bool:
    try:
        int(somStr)
    except:
        return False
    return True

def isFloat(somStr: str) -> bool:
    try:
        float(somStr)
    except:
        return False
    return True

def getLang(ex):
    for lang in fileExtension:
        for e in fileExtension[lang]:
            if ex == e:
                return lang

    return "?"

def extractConfigValue(prefix:str, text:str, problem:str):
    prefixHead = prefix.lower() + ":"
    assert prefixHead in text, f"{prefix} config not found in README.md in {problem} problem folder!\nPlease add the time config in README.md!"

    prefixIndex = text.find(prefixHead)
    prefixEndIndex = text.find("\n", prefixIndex)
    return text[prefixIndex + len(prefixHead):prefixEndIndex].strip()


EXAMPLE_HEADER = """
/*
mode : classic
expected : ??????????
score : 0
ignore : false (optional)
*/
"""

EXAMPLE_PYTHON_HEADER = """
########### HEADER ############
# mode : classic
# expected : ??????????
# score : 0
###############################
"""

if __name__ == "__main__":
    
    testEnv() #? in main grader
    testCodeDir = "./test/codes"
    testProblemsDir = "./test/problems"

    thisTime = time.localtime(time.time())

    allTestSourceCodeProblems = [p for p in os.listdir(testCodeDir) if isdir(joinPath(testCodeDir, p)) and isInt(p)]
    crt = 0
    failedTests = []

    for testPIndex, testP in enumerate(allTestSourceCodeProblems):
        printTest("PROBLEM", f"{testP}")

        assert isdir(joinPath(testProblemsDir, testP)), f"Problem {testP} not found in {testProblemsDir}\nPlease create the problem or remove the folder in {testCodeDir}!"
        assert isfile(joinPath(testProblemsDir, testP, "README.md")), f"README.md not found in problem {testP} folder!\nPlease create README.md in problem folder!"

        readmeText = fileRead(joinPath(testProblemsDir, testP, "README.md")).lower().replace(" ","")
        assert "##problem config (DON'T DELETE THIS SECTION)".lower().replace(" ", "") in readmeText, f"Problem config not found in README.md in problem {testP} folder!\nPlease add the config in README.md!"
        
        configTime = extractConfigValue("Time", readmeText, testP)
        configMemory = extractConfigValue("Memory", readmeText, testP)
        configTestcase = extractConfigValue("Testcase", readmeText, testP)

        assert isFloat(configTime), f"Time config in README.md in problem {testP} folder is not a number! ('{configTime}')\nPlease add the time config in README.md!"
        assert isInt(configMemory), f"Memory config in README.md in problem {testP} folder is not an integer! ('{configMemory}')\nPlease add the memory config in README.md!"

        configTime, configMemory = float(configTime), int(configMemory)

        print(f"Time : {configTime}")
        print(f"Memory : {configMemory}")
        print(f"Testcase : {configTestcase}")

        print(joinPath(testCodeDir, testP))
        print(os.listdir(joinPath(testCodeDir, testP)))

        allTestSourceCodeFiles = [f for f in os.listdir(joinPath(testCodeDir, testP)) if isfile(joinPath(testCodeDir, testP, f)) and getLang(f[f.find(".")+1:].strip()) != "?"]
        allTestSourceCodeFiles = sorted(allTestSourceCodeFiles)

        for indexFile, sFile in enumerate(allTestSourceCodeFiles):
            orderLabel = f"{testPIndex + 1}/{len(allTestSourceCodeProblems)} | {indexFile+1}/{len(allTestSourceCodeFiles)}"
            printTest(orderLabel, f"P{testP} : {sFile}...\n")
            
            filePathLabel = joinPath(testCodeDir, testP, sFile)
            sourceCode = fileRead(joinPath(testCodeDir, testP, sFile))
            lang = getLang(sFile[sFile.find(".")+1:].strip())

            #get info from header of source code
            if lang != "python":
                assert "/*" in sourceCode and "*/" in sourceCode, f"Info not found in file {filePathLabel}!\nPlease add the info in the header of the source code!\nExample:\n{EXAMPLE_HEADER}"
                headerIndex = sourceCode.find("/*")
                headerEndIndex = sourceCode.find("*/")
                header = sourceCode[headerIndex:headerEndIndex]
            else:
                assert "########### HEADER ############" in sourceCode and "###############################" in sourceCode, f"Info not found in file {filePathLabel} folder!\nPlease add the info in the header of the source code!\nExample:\n{EXAMPLE_PYTHON_HEADER}"
                headerIndex = sourceCode.find("########### HEADER ############")
                headerEndIndex = sourceCode.find("###############################")
                header = sourceCode[headerIndex:headerEndIndex]

            headerLines = header.strip().split("\n")
            requiredHeaders = ["mode", "expected", "score"]
            additionalHeaders = ["ignore"]
            headerInfo = {}
            for h in (requiredHeaders + additionalHeaders):
                for l in headerLines:
                    if h in l and ":" in l:
                        headerInfo[h] = l[l.find(":")+1:].strip()
                        break
                
                if h in requiredHeaders:
                    assert h in headerInfo, f"{h} not found in header of file {filePathLabel}!\nPlease add the info in the header of the source code!\nExample:\n{EXAMPLE_HEADER}"
            
            assert isInt(headerInfo["score"]), f"Score in header of file {filePathLabel} is not an integer! ('{headerInfo['score']}')\nPlease add the score in the header of the source code!\nExample:\n{EXAMPLE_HEADER}"
            isIgnore = "ignore" in headerInfo and headerInfo["ignore"].lower() == "true"

            testSubmit(crt, joinPath(testProblemsDir, testP), int(
                testP), sourceCode, configTestcase, headerInfo["mode"], lang, configMemory, configTime)
            

            if lastResult.result == headerInfo["expected"]:
                printPass("Result", f"Pass : {lastResult.result}")
            else:
                printFail("Result", f"Fail...\nExpected : {headerInfo['expected']}\nGot      : {lastResult.result}")
                failedTests.append(FailedTestDTO(
                    testP,
                    filePathLabel,
                    f"Result Fail...\nExpected : {headerInfo['expected']}\nGot      : {lastResult.result}",
                    isIgnore
                ))
            
            if lastResult.score == int(headerInfo["score"]):
                printPass("Score", f"Pass : {lastResult.score}")
            else:
                printFail("Score", f"Fail...\nExpected : {headerInfo['score']}\nGot      : {lastResult.score}")
                failedTests.append(FailedTestDTO(
                    testP,
                    filePathLabel,
                    f"Score Fail...\nExpected : {headerInfo['score']}\nGot      : {lastResult.score}",
                    isIgnore
                ))
            crt += 1

    printTest("TEST", "All tests finished!")
    print("----------------------------------------------")
    crt = 1
    #display all failed tests
    if any([not f.ignore for f in failedTests]):
        printFail("TEST", "Some tests failed!")
        for f in failedTests:
            if f.ignore:
                continue
            printFail(f"#{crt}", f.file)
            printFail("Message", f.message)
            print()
            crt += 1
    
    crt = 1
    if any([f.ignore for f in failedTests]):
        printWarning("TEST", "Some tests failed but can be ignored")
        for f in failedTests:
            if not f.ignore:
                continue
            printWarning(f"#{crt}", f.file)
            printWarning("Message", f.message)
            print()
            crt += 1



    if any([not f.ignore for f in failedTests]):
        exit(1)
    elif any([f.ignore for f in failedTests]):
        printPass("TEST", "Tests passed successfully!")
    else:
        printPass("TEST", "All tests passed successfully!")