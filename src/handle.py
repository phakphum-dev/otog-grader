import codecs
from constants import bcolors, langarr
import os
import signal
import time
import subprocess
from os import path
from pathlib import Path
from random import randint

MAX_ERROR_LINE = 200


def testEnv():
    if not path.exists("env"):
        os.mkdir("env")


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


def prepareEnv(problemId):

    # clear env

    envFiles = os.listdir("env/")
    for ffile in envFiles:
        os.system(f"rm env/{ffile}")


def createSourceCode(sourceCode, language):
    srcPath = f"""./env/temp{getRandomName(5)}.{langarr[language]["extension"]}"""
    fileWrite(srcPath, sourceCode)
    return srcPath


def create(userId, language, sourcePath, problemId):

    result = None
    compilecmd = langarr[language]["compile"].replace(
        "[sourcePath]", sourcePath)
    os.system(compilecmd)

    if not os.path.exists("env/out"):
        return "Compilation Error"
    return result


def errMsgHandle(errMes: str) -> str:

    errLines = errMes.split("\n")
    if len(errLines) > MAX_ERROR_LINE:
        errMes = "\n".join(
            errLines[:MAX_ERROR_LINE]) + f"\n\nand {len(errLines) - MAX_ERROR_LINE} more lines..."
    return errMes


def execute(userId, problemId, testcase, timeLimit, memoryLimit, language, sourcePath):
    inputFile = (
        f" <source/{problemId}/{testcase}.in 1>env/output.txt 2>env/error.txt"
    )
    cmd = f"ulimit -v {str(memoryLimit)}; {langarr[language]['execute']}; exit;"
    cmd = cmd.replace("[inputfile]", inputFile)
    cmd = cmd.replace("[sourcePath]", sourcePath)
    if os.path.exists("env/error.txt"):
        os.system("chmod 775 env/error.txt")
    if os.path.exists("env/output.txt"):
        os.system("chmod 775 env/output.txt")
    starttime = time.time()
    proc = subprocess.Popen([cmd], shell=True, preexec_fn=os.setsid)
    try:
        proc.communicate(timeout=(timeLimit / 1000))
        t = proc.returncode
    except subprocess.TimeoutExpired:
        t = 124
    endtime = time.time()
    timediff = endtime - starttime
    if os.path.exists("/proc/" + str(proc.pid)):
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    return t, timediff


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


def getTypeJudge(problemId):
    return "standard"


def getVerdict(problemId, userPath, solPath, testCase, srcPath, judgeType):
    # Standard Judge
    return stdcmpfunc(userPath, solPath) and "P" or "-"
