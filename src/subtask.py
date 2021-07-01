import ast
from constants import bcolors


def parseSqBr(content: str):
    content = content.strip()
    oIndex = 0
    mxTestCase = 0
    res = []
    while content.find("[", oIndex) != -1:
        sIndex = content.find("[", oIndex)
        if content.find("]", oIndex) == -1:
            return "expected ']' to close '['\nBlame Problem author", -1
        eIndex = content.find("]", oIndex)
        oIndex = eIndex+1

        try:
            list(map(int, content[sIndex+1:eIndex].split(',')))
        except Exception as e:
            return f"Error durring convert from text to int\n{e}\nBlame Problem author", -1

        mxTestCase = max(mxTestCase, max(
            map(int, content[sIndex+1:eIndex].split(','))))

        res.append(list(map(int, content[sIndex+1:eIndex].split(','))))
    return res, mxTestCase


def validRequire(data):
    n = len(data)
    graph = [[] for i in range(n+3)]
    inOrder = [0 for i in range(n+3)]
    state = [False for i in range(n+3)]

    for i in range(n):
        if "require" in data[i+1]:
            if type(data[i+1]["require"]) == type(69) and data[i+1]["require"] <= n:
                graph[i+1].append(data[i+1]["require"])
                inOrder[data[i+1]["require"]] += 1
            elif type(data[i+1]["require"]) == type(list()):
                for x in data[i+1]["require"]:
                    if type(x) == type(69) and x <= n:
                        graph[i+1].append(x)
                        inOrder[x] += 1

    while True:
        zero = -1
        isCom = True

        for i in range(n):
            if inOrder[i+1] == 0 and state[i+1] == False:
                zero = i+1
            elif inOrder[i+1] != 0:
                isCom = False

        if zero == -1 and not isCom:  # no Topo
            return False

        if isCom:
            return True

        for nextNode in graph[zero]:
            inOrder[nextNode] -= 1
        state[zero] = True


def compile(content: str):
    content = content.strip()
    content = content.replace("true", "True").replace("false", "False")

    if content.startswith("["):

        result, maxCase = parseSqBr(content)
        if maxCase == -1:
            return -1, result
        subtaskData = dict()
        ind = 1
        for sub in result:
            subtaskData[ind] = {
                "group": True,
                "score": len(sub)
            }
            ind += 1
        return maxCase, (result, subtaskData)
    if content.startswith("{"):
        try:
            dataJson = ast.literal_eval(content)
        except Exception as e:
            return -1, f"Invalid json?...\n{e}\nBlame Problem author"

        if "subtask" not in dataJson:
            return -1, f"expected 'subtask'!"

        if type(dataJson["subtask"]) != type("Hello"):
            return -1, f"expected string in subtask!"

        subtask, mxTestcase = parseSqBr(dataJson["subtask"])

        if mxTestcase == -1:
            return -1, subtask

        isAllSubtask = True
        for i in range(len(subtask)):
            if i+1 not in dataJson:
                isAllSubtask = False
                break

            if type(dataJson[i+1]) != type(dict()):
                isAllSubtask = False
                break

        subtaskData = dict()
        if isAllSubtask:
            for i in range(len(subtask)):
                subtaskData[i+1] = dict(dataJson[i+1])
        else:
            print(
                f"[ {bcolors.WARNING}SUBTASK{bcolors.RESET} ] Invalid subtask data, so use default instead")
            ind = 1
            for sub in subtask:
                subtaskData[ind] = {
                    "group": True,
                    "score": len(sub)
                }
                ind += 1

        for i in range(1, len(subtask)+1):
            if "require" in subtaskData[i]:
                if type(subtaskData[i]["require"]) != type(69) and type(subtaskData[i]["require"]) != type([]):
                    subtaskData[i]["require"] = []
                    print(
                        f"[ {bcolors.WARNING}SUBTASK{bcolors.RESET} ] Invalid require data in subtask {i}, expected number or list")

            if "score" in subtaskData[i]:
                if type(subtaskData[i]["score"]) != type(69) and type(subtaskData[i]["score"]) != type(69.2):
                    subtaskData[i]["score"] = len(subtask[i-1])
                    print(
                        f"[ {bcolors.WARNING}SUBTASK{bcolors.RESET} ] Invalid score data in subtask {i}, so use score by counting")

            if "group" in subtaskData[i]:
                if type(subtaskData[i]["group"]) != type(False):
                    subtaskData[i]["group"] = True
                    print(
                        f"[ {bcolors.WARNING}SUBTASK{bcolors.RESET} ] Invalid group data in subtask {i}, expected true or false. So use True instead")

        if not validRequire(subtaskData):
            return -1, f"Invalid require (found loop in require)"

        return mxTestcase, (subtask, subtaskData)

    return -1, "Invalid subtask format :(:(:(\nBlame Problem author"


def finalResult(nowVerdict, bigSubtaskData):

    subtask, subtaskData = bigSubtaskData
    n = len(subtask)
    finalVerdict = ["" for i in range(n+3)]
    isFinal = [False for i in range(n+3)]
    isAccept = [False for i in range(n+3)]
    finalScore = 0
    finalMaxScore = 0

    while True:
        isComplete = True
        for i in range(1, n+1):
            if not isFinal[i]:
                isReady = True
                if "require" in subtaskData[i]:
                    if type(subtaskData[i]["require"]) == type(69) and subtaskData[i]["require"] <= n:
                        isReady = isFinal[subtaskData[i]["require"]]
                    elif type(subtaskData[i]["require"]) == type([]):
                        for req in subtaskData[i]["require"]:
                            if type(req) == type(69) and req <= n:
                                isReady = isReady and isFinal[req]
                if isReady:
                    if "require" in subtaskData[i]:
                        allReq = []
                        if type(subtaskData[i]["require"]) == type(69) and subtaskData[i]["require"] <= n:
                            allReq.append(subtaskData[i]["require"])
                        elif type(subtaskData[i]["require"]) == type([]):
                            for req in subtaskData[i]["require"]:
                                if type(req) == type(69) and req <= n:
                                    allReq.append(req)

                        isSkiped = False
                        for req in allReq:
                            if not isAccept[req]:
                                isSkiped = True

                        if isSkiped:
                            allCrt = len(subtask[i-1])
                            correct = 0
                            finalVerdict[i] = "S"*allCrt
                            isFinal[i] = True
                            isAccept[i] = False
                            if "score" in subtaskData[i]:
                                finalMaxScore += float(subtaskData[i]["score"])
                            else:
                                finalMaxScore += allCrt
                            isComplete = isComplete and isFinal[i]
                            continue

                    allCrt = len(subtask[i-1])
                    correct = 0
                    thisVerdict = ""
                    for case in subtask[i-1]:
                        if nowVerdict[case-1] == "P":
                            correct += 1
                        thisVerdict += nowVerdict[case-1]
                    if "group" in subtaskData[i] and subtaskData[i]["group"]:
                        if correct != allCrt:
                            correct = 0

                    if "score" in subtaskData[i]:
                        finalScore += correct * \
                            float(subtaskData[i]["score"]) / allCrt
                        finalMaxScore += float(subtaskData[i]["score"])
                    else:
                        finalScore += correct
                        finalMaxScore += allCrt

                    finalVerdict[i] = thisVerdict
                    isFinal[i] = True
                    isAccept[i] = (correct == allCrt)

            isComplete = isComplete and isFinal[i]

        if isComplete:
            finalVerdictStr = ""
            for i in range(1, n+1):
                finalVerdictStr += f"[{finalVerdict[i]}]"
            return finalVerdictStr, finalScore, finalMaxScore


if __name__ == "__main__":

    mxCase, dataSub = compile("""{
      "subtask": "[1,2,3][4,5,6][7,8,9,10]",
      1: {
        "group": true,
        "score": 10,
      },
      2: {
        "group": true,
        "score": 11.4,
        "require" : 3
      },
      3: {
        "group": true,
        "score": 45,
      },
    }""")
    print(dataSub)
    finalVer, score, maxScore = finalResult("---PPPPPP-", dataSub)
    print("Result :", finalVer)
    print("Score :", score, "/", maxScore)
