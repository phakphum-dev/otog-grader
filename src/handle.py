import codecs
from constants import bcolors, langarr
import os
import signal
import time
import subprocess
from pathlib import Path

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
            "SIGSEGV||Segmentation fault (core dumped)\n" + fileRead("env/error.txt"),
        )
    elif t == 136:
        errCode = "SIGFPE"
        fileWrite(
            "env/error.txt",
            "SIGFPE||Floating point exception\n" + fileRead("env/error.txt"),
        )
    elif t == 134:
        errCode = "SIGABRT"
        fileWrite("env/error.txt", "SIGABRT||Aborted\n" + fileRead("env/error.txt"))
    elif t != 0:
        errCode = "NZEC"
        fileWrite(
            "env/error.txt",
            "NZEC||return code : " + str(t) + "\n" + fileRead("env/error.txt"),
        )
    return errCode


def createSourceCode(sourceCode, language):
    if os.path.exists("env/temp.*"):
        os.system("rm env/temp.*")
    fileWrite(f"""env/temp.{langarr[language]["extension"]}""", sourceCode)


def create(userId, language):
    if os.path.exists("env/out"):
        os.system("rm env/out")
    if language not in ["c", "cpp"]:
        return
    result = None
    compilecmd = langarr[language]["compile"]
    os.system(compilecmd)
    if not os.path.exists("env/out"):
        result = "Compilation Error"
    return result


def execute(userId, problemId, testcase, timeLimit, memoryLimit, language):
    inputFile = (
        f" <source/{problemId}/{testcase}.in 1>env/output.txt 2>env/error.txt"
    )
    cmd = f"ulimit -v {str(memoryLimit)}; {langarr[language]['execute']}; exit;"
    cmd = cmd.replace("[inputfile]", inputFile)
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
    PROBLEM_PATH = f"./source/{problemId}"
    if Path(f"{PROBLEM_PATH}/interactive_script.py").is_file():
        return "ogogi"
    return "standard"

def getVerdict(problemId, userPath, solPath):
    PROBLEM_PATH = f"./source/{problemId}"
    judgeType = getTypeJudge(problemId)

    #OGOGI Judge
    if judgeType == "ogogi":
        thisCmd = f"python3 {PROBLEM_PATH}/interactive_script.py {userPath}"
        proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid, stdout=subprocess.PIPE)
        result,_ = proc.communicate()
        t = proc.returncode
        if os.path.exists("/proc/" + str(proc.pid)):
            #RIP
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        
        result = result.decode(encoding="utf8")
        if t != 0 or len(result.strip()) != 1:
            return "!"#Judge Error... Bruh
        return result.strip()
    

    #Standard Judge
    return stdcmpfunc(userPath, solPath) and "P" or "-"

    

