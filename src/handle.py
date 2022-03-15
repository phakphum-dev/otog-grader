import codecs
import os
import signal
import time
import subprocess
import yaml
from os import path
from pathlib import Path
from random import randint

from message import *
import config
import cmdManager as langCMD

MAX_ERROR_LINE = int(config.get("grader", "max_error_line"))


def testEnv():
    if not path.exists("env"):
        os.mkdir("env")

def initIsolate():

    os.system("isolate --cg --cleanup")

    p = subprocess.Popen("isolate --cg --init",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pData = p.communicate()
    boxPath = pData[0].decode().strip()
    stdErr = pData[1].decode().strip()
    returnCode = p.returncode

    if returnCode != 0:
        printFail("isolate","Can't init")
        print(stdErr)
        printBlod("isolate","isolate isn't used")
        return None
    return boxPath + "/box"

def isolateMetaReader(content:str):
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

    #? check problem's custom command.yaml
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
        compilecmd = langCMD.get(language,"compile")
    else:
        printHeader("COMPILE", f"use command from command.yaml")
    compilecmd = compilecmd.replace("[sourcePath]", sourcePath).replace("[problemPath]", f"source/{problemId}")
    
   

    if isoPath != None:
        compilecmd = compilecmd.replace("[binPath]", f"{isoPath}/out")
        realEnv = isoPath
    else:
        compilecmd = compilecmd.replace("[binPath]", "env/out")
        realEnv = "env"
    compilecmd = compilecmd.replace("[env]", realEnv)


    #? Compile With time limit of 30 seconds
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
    return errMes


def execute(userId, problemId, testcase, timeLimit, memoryLimit, language, sourcePath, isoPath):
    
    if isoPath != None: #? Use isolate to execute
        
        inputFile = f"< ../source/{problemId}/{testcase}.in"
        cmd = "cd env; "
        cmd += "isolate --cg --meta=isoResult.txt --stdout=output.txt --stderr=error.txt "
        cmd += f"--time={timeLimit / 1000} --mem={memoryLimit} "
        cmd += f"--run -- {langCMD.get(language,'execute')} "
        cmd += f"{inputFile} ; exit"

        cmd = cmd.replace("[ioRedirect]", "")
        cmd = cmd.replace("[sourcePath]", sourcePath.replace(f"{isoPath}/", ""))
        cmd = cmd.replace("[binPath]", "./out")
        cmd = cmd.replace("[uBin]", "/usr/bin/")

        p = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.communicate()

        if not os.path.exists(f"env/isoResult.txt"):
            printFail("GRADER","isoResult.txt not found")
            printFail("GRADER","ABORT PROCESS!!!")
            exit(1)
        
        try:
            with open(f"env/isoResult.txt", "r") as f:
                isoResult = f.read()
            isoResult = isolateMetaReader(isoResult)
        except:
            printFail("GRADER","can't read isoResult.txt")
            printFail("GRADER","ABORT PROCESS!!!")
            exit(1)
        
        
        if "status" in isoResult and isoResult["status"] == "XX":
            printFail("GRADER","internal error of the sandbox")
            printFail("GRADER","ABORT PROCESS!!!")
            exit(1)
        
        if "status" in isoResult and isoResult["status"] == "TO":
            exitCode = 124
        elif "exitsig" in isoResult:
            exitCode = int(isoResult["exitsig"])
        elif "exitcode" in isoResult:
            exitCode = int(isoResult["exitcode"])
        else:
            exitCode = 0

        timeUse = float(isoResult["time"])
        memUse = int(isoResult["cg-mem"]) #TODO : CHECK IS IT RIGHT?
        os.system("chmod 500 env")
        os.system("chmod 775 env/output.txt")
        os.system("chmod 775 env/error.txt")
        os.system(f"cp {isoPath}/output.txt env/output.txt")
        os.system(f"cp {isoPath}/error.txt env/error.txt")


        return exitCode, timeUse, memUse
    else:
    
        ioFile = (
            f"< ../source/{problemId}/{testcase}.in 1>output.txt 2>error.txt"
        )
        cmd = f"cd env;ulimit -v {str(memoryLimit)}; {langCMD.get(language,'execute')}; exit;"
        cmd = cmd.replace("[ioRedirect]", ioFile)
        cmd = cmd.replace("[sourcePath]", sourcePath.replace("env/", ""))

        
        cmd = cmd.replace("[binPath]", "./out")
        cmd = cmd.replace("[uBin]", "")
        
        os.system("chmod 500 env")
        os.system("chmod 775 env/error.txt")
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
        os.system("chmod -R 750 env")
        return t, timediff, None


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
    if Path(f"{PROBLEM_PATH}/check.cpp").is_file():
        thisCmd = f"g++ {PROBLEM_PATH}/check.cpp -O2 -std=c++17 -fomit-frame-pointer -o {PROBLEM_PATH}/binCheck"
        proc = subprocess.Popen([thisCmd], shell=True, preexec_fn=os.setsid)
        proc.communicate()
        if os.path.exists("/proc/" + str(proc.pid)):
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # RIP
        return "check.cpp"
    return "standard"

def getMissingSeqNumberFile(pathTo:str, extension:str, number:int):
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
    if judgeType == "ogogi":
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
    elif judgeType == "check.cpp":
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
