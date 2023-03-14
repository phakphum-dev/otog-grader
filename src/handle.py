import codecs
import os
import signal
import time
import subprocess
import yaml
from os import path
from pathlib import Path
from random import randint
from DTO.result import ResultDTO
from DTO.submission import SubmissionDTO
from constants.LoggingMsg import Logging

from message import *
from constants.osDotEnv import *
import cmdManager as langCMD
from constants.Enums import *

MAX_ERROR_LINE = int(osEnv.GRADER_MAX_ERROR_LINE)


def strToBool(value: str) -> bool:
    if value.lower() == "false" or value.lower() == "f":
        return False
    return True


def testEnv():
    if not path.exists("env"):
        os.mkdir("env")


def prepareLoging(sub: SubmissionDTO):
    if strToBool(osEnv.GRADER_ENABLE_OFFLINE_LOGGING) == False:
        return

    thisTime = time.localtime(time.time())
    folderName = f"{thisTime.tm_year}{thisTime.tm_mon:02d}{thisTime.tm_mday:02d}"
    if not path.exists("./Logging"):
        os.mkdir("./Logging")

    if not path.exists(f"./Logging/{folderName}"):
        os.mkdir(f"./Logging/{folderName}")

    replaces = [
        ("subId", sub.id),
        ("userId", sub.userId),
        ("lang", sub.language),
        ("proId", sub.problemId),
        ("proSec", sub.timeLimit),
        ("proMem", sub.memoryLimit),
        ("code", sub.sourceCode),
        # ("resScore"),
        # ("resVerdict"),
        # ("resTime"),
        # ("resMem"),
        # ("resErrMsg"),
    ]
    strContent = Logging.noResult
    for e in replaces:
        strContent = strContent.replace(f"<!{e[0]}!>", str(e[1]))

    fileWrite(f"./Logging/{folderName}/{sub.id} waiting.md", strContent)


def resultLoging(sub: SubmissionDTO, res: ResultDTO):
    if strToBool(osEnv.GRADER_ENABLE_OFFLINE_LOGGING) == False:
        return

    thisTime = time.localtime(time.time())
    folderName = f"{thisTime.tm_year}{thisTime.tm_mon:02d}{thisTime.tm_mday:02d}"

    replaces = [
        ("subId", sub.id),
        ("userId", sub.userId),
        ("lang", sub.language),
        ("proId", sub.problemId),
        ("proSec", sub.timeLimit),
        ("proMem", sub.memoryLimit),
        ("code", sub.sourceCode),
        ("resScore", res.score),
        ("resVerdict", res.result),
        ("resTime", res.sumTime),
        ("resMem", res.memUse),
        ("resErrMsg", res.errmsg),
    ]
    strContent = Logging.afterResult
    for e in replaces:
        strContent = strContent.replace(f"<!{e[0]}!>", str(e[1]))

    os.remove(f"./Logging/{folderName}/{sub.id} waiting.md")
    fileWrite(f"./Logging/{folderName}/{sub.id}.md", strContent)


def initIsolate(useControlGroup:bool = True):


    os.system(f"isolate {useControlGroup and '--cg' or ''} --cleanup")

    p = subprocess.Popen(f"isolate {useControlGroup and '--cg' or ''} --init", shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pData = p.communicate()
    boxPath = pData[0].decode().strip()
    stdErr = pData[1].decode().strip()
    returnCode = p.returncode

    if returnCode != 0:
        printFail("isolate", "Can't init")
        print(stdErr)
        printBlod("isolate", "isolate isn't used")
        return None
    return boxPath + "/box"


def isolateMetaReader(content: str):
    content = content.strip().split("\n")
    resultData = dict()
    for line in content:
        if line.find(":") != 1:
            chunk = line.split(":")
            resultData[chunk[0].strip()] = ":".join(chunk[1:]).strip()

    return resultData


def fileRead(filename):
    try:
        with codecs.open(filename, "r", "utf-8") as f:
            return f.read().replace("\r", "")
    except:
        return ""


def fileWrite(filename, data):
    with codecs.open(filename, "w", "utf-8") as f:
        f.write(data.replace("\r", ""))


def error(t):
    errCode = None
    if t == 124:
        errCode = "TLE"
        fileWrite("env/error.txt", "Time Limit Exceeded - Process killed.")
    elif t == 139:
        errCode = "SIGSEGV"
        fileWrite(
            "env/error.txt",
            "SIGSEGV||Segmentation fault (core dumped)\n" +
            fileRead("env/error.txt"),
        )
    elif t == 136:
        errCode = "SIGFPE"
        fileWrite(
            "env/error.txt",
            "SIGFPE||Floating point exception\n" + fileRead("env/error.txt"),
        )
    elif t == 134:
        errCode = "SIGABRT"
        fileWrite("env/error.txt", "SIGABRT||Aborted\n" +
                  fileRead("env/error.txt"))
    elif t == 69696969:
        errCode = "ISOERR"
    elif t != 0:
        errCode = "NZEC"
        fileWrite(
            "env/error.txt",
            "NZEC||return code : " + str(t) + "\n" + fileRead("env/error.txt"),
        )
    return errCode


def getRandomName(lenAl: int):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    result = ""
    for i in range(lenAl):
        result += alphabet[randint(0, len(alphabet)-1)]
    return result


def prepareEnv(problemId, isoPath):

    if isoPath != None:
        # Grab custom library
        problemFile = os.listdir(f"./source/{problemId}")
        for ffile in problemFile:
            if ffile.endswith(".c") or ffile.endswith(".h") \
                    or (ffile.endswith(".cpp") and not ffile == "check.cpp") \
                    or (ffile.endswith(".py") and not ffile == "interactive_script.py"):
                os.system(f"cp ./source/{problemId}/{ffile} {isoPath}/")
    else:

        # clear env
        if path.exists("env/__pycache__"):
            os.system(f"rm -r env/__pycache__")

        envFiles = os.listdir("env/")
        for ffile in envFiles:
            os.system(f"rm env/{ffile}")

        # Grab custom library
        problemFile = os.listdir(f"./source/{problemId}")
        for ffile in problemFile:
            if ffile.endswith(".c") or ffile.endswith(".h") \
                    or (ffile.endswith(".cpp") and not ffile == "check.cpp") \
                    or (ffile.endswith(".py") and not ffile == "interactive_script.py"):
                os.system(f"cp ./source/{problemId}/{ffile} ./env/")


def createSourceCode(sourceCode, language, isoPath):

    resPath = "./env"
    if isoPath != None:
        resPath = isoPath

    srcPath = f"""{resPath}/temp{getRandomName(5)}.{langCMD.get(language,"extension")}"""
    fileWrite(srcPath, sourceCode)
    return srcPath


def create(userId, language, sourcePath, problemId, isoPath):

    commandData = None
    compilecmd = None

    # ? check problem's custom command.yaml
    if os.path.exists(f"source/{problemId}/command.yaml"):
        try:
            with open(f"source/{problemId}/command.yaml", "r") as f:
                command = f.read()
            commandData = yaml.load(command, Loader=yaml.FullLoader)
        except:
            printWarning("COMPILE", "Can't read command.yaml")

    if type(commandData) == type(dict()):
        if language in commandData:
            if "compile" in commandData[language]:
                compilecmd = commandData[language]["compile"]
            else:
                printWarning(
                    "COMPILE", f"'compile' not found in lang {language}")
        else:
            printWarning("COMPILE", f"{language} not found in command.yaml")

    if compilecmd == None:
        compilecmd = langCMD.get(language, "compile")
    else:
        printHeader("COMPILE", f"use command from command.yaml")
    compilecmd = compilecmd.replace("[sourcePath]", sourcePath).replace(
        "[problemPath]", f"source/{problemId}")

    if isoPath != None:
        compilecmd = compilecmd.replace("[binPath]", f"{isoPath}/out")
        realEnv = isoPath
    else:
        compilecmd = compilecmd.replace("[binPath]", "env/out")
        realEnv = "env"
    compilecmd = compilecmd.replace("[env]", realEnv)

    # ? Compile With time limit of 30 seconds
    isTLE = False
    proc = subprocess.Popen([compilecmd], shell=True, preexec_fn=os.setsid)
    try:
        proc.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        isTLE = True
    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    if isTLE:
        return "Compilation TLE"

    if language == "python":
        if os.path.exists(f"{realEnv}/error.txt") and fileRead(f"{realEnv}/error.txt").strip():
            return "Compilation Error"
    else:
        if not os.path.exists(f"{realEnv}/out"):
            return "Compilation Error"

    # prepare output and error text file
    os.system("touch env/error.txt")
    os.system("touch env/output.txt")
    return None


def errMsgHandle(errMes: str) -> str:
    # Python
    if errMes.find("During handling of the above exception, another exception occurred:") != -1:
        errMes = errMes[:errMes.find(
            "During handling of the above exception, another exception occurred:")]

    errLines = errMes.split("\n")
    if len(errLines) > MAX_ERROR_LINE:
        errMes = "\n".join(
            errLines[:MAX_ERROR_LINE]) + f"\n\nand {len(errLines) - MAX_ERROR_LINE} more lines..."

    pathCensor = ["./env", "/var/local/lib/isolate/0/box"]
    for e in pathCensor:
        errMes = errMes.replace(e, "")

    return errMes


def stdcmpfunc(fname1, fname2):
    try:
        with open(fname1) as f1, open(fname2) as f2:
            while True:
                f1_line = f1.readline()
                f2_line = f2.readline()
                if f1_line == "" and f2_line == "":
                    return True
                if f1_line.rstrip() != f2_line.rstrip():
                    return False
    except:
        return False


def getMissingSeqNumberFile(pathTo: str, extension: str, number: int):
    """This function will check every file in <pathTo>/{i}.<extension>
    for {i} range from 1 to <number>
    This function will return the list of missing files


    eg. isSeqNumberFile("testP", "in", 5) it will check testP/1.in, testP/2.in, testP/3.in, testP/4.in and testP/5.in 
    It will return [] if 5 of them are exist
    but if one of them missing like 4.in is missing, It will return [4]"""

    result = []

    for i in range(number):
        if not Path(f"{pathTo}/{i + 1}.{extension}").is_file():
            result.append(i+1)

    return result


def getVerdict(problemId, userPath, solPath, testCase, srcPath, judgeType):
    PROBLEM_PATH = f"./source/{problemId}"

    # OGOGI Judge
    if judgeType == JudgeType.ogogi:
        thisCmd = f"python3 {PROBLEM_PATH}/interactive_script.py {userPath} {PROBLEM_PATH}/ {testCase}"
        proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, _ = proc.communicate()
        t = proc.returncode
        if os.path.exists("/proc/" + str(proc.pid)):
            # RIP
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

        result = result.decode(encoding="utf8")
        if t != 0 or len(result.strip()) != 1:
            return "!"  # Judge Error... Bruh
        return result.strip()
    elif judgeType == JudgeType.cppCheck:
        if not Path(f"{PROBLEM_PATH}/binCheck").is_file():
            return "!"

        os.system(f"cp {userPath} ./output.txt")
        thisCmd = f"{PROBLEM_PATH}/binCheck {solPath} {PROBLEM_PATH}/{testCase}.in {srcPath}"
        proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        if os.path.exists("/proc/" + str(proc.pid)):
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # RIP
        t = proc.returncode

        result = fileRead(f"./grader_result.txt")
        try:
            os.system("rm ./output.txt")
            os.system("rm ./grader_result.txt")
        except:
            pass

        if t != 0 or len(result.strip()) != 1:
            return "!"  # Judge Error... Bruh
        return result.strip().replace("W", "-")

    # Standard Judge
    return stdcmpfunc(userPath, solPath) and "P" or "-"
