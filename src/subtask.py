from DTO.subtask import *
import json

from message import *


def getSeq(data: list) -> list:
    n = len(data)
    seq = []
    adj = [[] for i in range(n)]
    inDeg = [0 for i in range(n)]
    zero = []

    for i, sub in enumerate(data):
        for u in sub.require:
            adj[u].append(i)
            inDeg[i] += 1

        if inDeg[i] == 0:
            zero.append(i)

    while zero:
        nowNode = zero.pop()
        seq.append(nowNode)

        for e in adj[nowNode]:
            inDeg[e] -= 1
            if inDeg[e] == 0:
                zero.append(e)

    if len(seq) != n:
        return []
    return seq


def parseNumFromStr(strContent: str, nNum: int = 1):
    nums = []
    l = 0
    while l < len(strContent):
        if strContent[l].isdigit():
            lastR = l
            for r in range(l + 1, len(strContent)):
                if strContent[l:(r + 1)].isdigit():
                    lastR = r
                else:
                    break
            nums.append(int(strContent[l:(lastR + 1)]))
            l = lastR + 1
        else:
            l += 1

    if len(nums) > nNum:
        nums = nums[:nNum]

    if len(nums) == 1:
        return nums[0]

    return nums


def tryJSONFormat(content: str):
    try:
        jsonData = json.loads(content)
    except Exception as e:
        return f"Invalid json format...\n{e}"

    return jsonData


def tryNumFormat(content: str):
    try:
        maxNum = int(content)
    except:
        return "Invalid num format... because can't convert to num (integer)"

    if maxNum <= 0:
        return "Invalid num format... number of testcase must greater than 0"

    return {
        "version": 1.0,
        "data": {
            "subtask 1": {
                "case": f"1-{maxNum}",
                "group": False,
                "score": 100
            },
        }
    }


def compile(content: str):
    content = content.strip()

    # * There are 2 format now
    # * 1. just num
    # * 2. number of testcase

    JSONResultData = tryJSONFormat(content)
    numResultData = tryNumFormat(content)

    if isinstance(JSONResultData, (int, float)):
        JSONResultData = "It's num data. NOT JSON"

    usedData = None
    if not isinstance(numResultData, str) and usedData == None:
        usedData = numResultData
    elif not isinstance(JSONResultData, str) and usedData == None:
        usedData = JSONResultData

    if usedData == None:
        # ? can't convert
        printFail("SUBTASK", "Can't convert with any format...")
        printFail("JSON", JSONResultData)
        printFail("NUM", numResultData)
        return None

    # ? Check Data
    if not isinstance(usedData, dict):
        printFail("SUBTASK", "Invalid subtask data...\nExpected Dict\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
        return None

    if "version" not in usedData:
        printFail("SUBTASK", "Invalid subtask data...\nExpected 'version'\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
        return None

    if "data" not in usedData:
        printFail("SUBTASK", "Invalid subtask data...\nExpected 'data'\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
        return None

    if not isinstance(usedData["data"], dict):
        printFail("SUBTASK", "Invalid subtask data...\nExpected Dict in 'Data'\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
        return None

    if len(usedData["data"]) == 0:
        printFail("SUBTASK", "Invalid subtask data...\nNo subtask data? rlly?\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
        return None

    for subN in usedData["data"]:
        if not isinstance(usedData["data"][subN], dict):
            printFail(
                "SUBTASK", f"Invalid subtask data...\nExpected Dict in {subN}\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
            return None

        if "case" not in usedData["data"][subN]:
            printFail(
                "SUBTASK", f"Invalid subtask data...\nExpected case in {subN}\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
            return None

        if not isinstance(usedData["data"][subN]["case"], str):
            printFail(
                "SUBTASK", f"Invalid subtask data...\nExpected 'string' case in {subN}\nsee https://github.com/phakphum-dev/otog-doc/blob/main/Problem/Subtask.md for more detail.")
            return None

    # ? prepare nameorder

    subtaskNumSet = set()
    subtaskName = []
    for s in usedData["data"]:
        numSubtaskName = parseNumFromStr(s)
        if numSubtaskName == []:
            printWarning(
                "SUBTASK", f"Invalid subtask name\n number of subtask not found (\"{s}\"). Skipping...")
            continue
        if numSubtaskName in subtaskNumSet:
            printWarning(
                "SUBTASK", f"Invalid subtask name\nfound duplicated number of subtask (\"{s}\").\nIt may not work property!")
        subtaskName.append(s)
        subtaskNumSet.add(numSubtaskName)

    subtaskNameToInd = {}
    subtaskNToInd = {}
    subtaskName = sorted(subtaskName, key=lambda x: parseNumFromStr(x))

    ind = 0
    for sName in subtaskName:
        subtaskNameToInd[sName] = ind
        subtaskNToInd[parseNumFromStr(sName)] = ind
        ind += 1

    result = ProblemTaskDTO(0, [], [])

    # ? grab a data

    for subN in subtaskName:
        thisSubData = SubtaskDTO(69, [], 69, False, [])

        # ? case
        cases = set()
        caseDataChunk = usedData["data"][subN]["case"].strip().split(",")
        for chunk in caseDataChunk:
            p = parseNumFromStr(chunk, 2)
            if isinstance(p, list):
                if p == []:
                    continue
                l, r = p
                if l > r:
                    l, r = r, l
                for i in range(l, r + 1):
                    cases.add(i)
            else:
                cases.add(p)
        cases = list(cases)
        cases = sorted(cases)
        thisSubData.cases = cases.copy()
        result.maxCase = max(result.maxCase, cases[-1])

        # ? score
        if "score" in usedData["data"][subN]:
            if isinstance(usedData["data"][subN]["score"], (float, int)):
                thisSubData.score = float(usedData["data"][subN]["score"])
            else:
                thisSubData.score = len(cases)
                printWarning(
                    "SUBTASK", f"Invalid score data in {subN}, so use score by counting")
        else:
            thisSubData.score = len(cases)

        # ? group
        if "group" in usedData["data"][subN]:
            if isinstance(usedData["data"][subN]["group"], bool):
                thisSubData.group = usedData["data"][subN]["group"]
            else:
                thisSubData.group = True
                printWarning(
                    "SUBTASK", f"Invalid group data in {subN}, expected true or false. So use True instead")
        else:
            thisSubData.group = True

        # ? require
        thisReq = []
        if "require" in usedData["data"][subN]:
            if isinstance(usedData["data"][subN]["require"], (int, list)):
                if isinstance(usedData["data"][subN]["require"], int):
                    thisReq = [usedData["data"][subN]["require"]]
                else:
                    thisReq = list(set(usedData["data"][subN]["require"]))

                for e in thisReq:
                    if e not in subtaskNToInd:
                        # ? require void subtask ... skipping
                        printWarning(
                            "SUBTASK", f"{subN} has require Subtask {e} which isn't exist.")
                        continue
                    thisSubData.require.append(subtaskNToInd[e])
            else:
                thisSubData.require = []
                printWarning(
                    "SUBTASK", f"Invalid require data in {subN}, expected number or list")
        else:
            thisSubData.require = []

        # ? last
        thisSubData.number = parseNumFromStr(subN)

        result.subtasks.append(thisSubData)

    # ? valid require and get sequence
    result.orderIndSubtask = getSeq(result.subtasks)
    if result.orderIndSubtask == []:
        printFail("SUBTASK", f"Invalid require data, Found loop in require")
        return None

    return result


if __name__ == "__main__":

    bruhData = compile("""10""")
    print(bruhData)
    if not bruhData == None:
        for s in bruhData.subtasks:
            print(s)
