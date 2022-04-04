from pathlib import Path
import configparser
from datetime import datetime
import tabulate

from handle import *
from DTO.submission import submissionDTO
import subtask
from message import *
import judge



def updateResult(subName, result, score, timeLen, memUse, comment):
    print(f"\n\n-------------End of submit {subName}-------------")
    print(f"result : {result}")
    print(f"score : {score}")
    print(f"timeLen : {timeLen}")
    print(f"memUse  : {memUse}")
    print(f"comment : {comment}")
    print(f"-----------------------------------------------")

def runCase(id, case):
    pass

fileExtension = {
    "c" : ["c","i"],
    "cpp" : ["cpp","cc","cxx","c++","hpp","hh","hxx","h++","h","ii"],
    "python" : ["py","rpy","pyw","cpy","gyp","gypi","pyi","ipy"]
}




def testSubmit(crt, subName, proId, srcCode: str, testcase, lang="cpp", mem=256, timeLim = 10):
    testEnv()
    nUser = crt * 100 + 69
    # If there is new payload
    submission = submissionDTO(
        nUser,
        nUser,
        proId,
        69,
        srcCode, lang, 100,
        timeLim * 1000, mem, testcase, "classic"
    )
    judge.startJudge(submission, updateResult, runCase)


if __name__ == "__main__":

    testCaseConfig = configparser.ConfigParser()
    testCaseConfig.read("testCodeDB.ini")

    def isInt(somStr: str) -> bool:
        try:
            int(somStr)
        except:
            return False
        return True
    
    def getLang(ex) : 
        for lang in fileExtension:
            for e in fileExtension[lang]:
                if ex == e:
                    return lang
        
        return "?"

    allPTestFolder = [x for x in os.listdir(
        f"./testCodes/") if os.path.isdir(f"./testCodes/{x}") and isInt(x)]
    
    crt = 0

    for testP in allPTestFolder:
        print(
            f"\n\n\n======================== Problem {testP} ========================\n\n")

        if testP not in testCaseConfig:
            print(f"No config in {testP}.... skiping!")
            print(f"TIP : you can config in testCodeDB.ini")
            continue
        
        if "TestCase" not in testCaseConfig[testP]:
            print(f"Please specify the number of test case ({testP}) in testCodeDB.ini")
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
            f"./testCodes/{testP}") if os.path.isfile(f"./testCodes/{testP}/{x}") and (getLang(x[x.find(".")+1:].strip()) != "?")]

        for sFile in srcFiles:
            print(f">>Testing : {sFile}...\n")
            codo = fileRead(f"./testCodes/{testP}/{sFile}")
            lang = getLang(sFile[sFile.find(".")+1:].strip())
            testSubmit(crt, sFile, int(
                testP), codo, testCaseConfig[testP]["TestCase"], lang, configMem, configTime)
            
            crt += 1
