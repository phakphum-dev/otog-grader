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


SUBTASK_URL_WIKI = "https://github.com/phakphum-dev/otog-doc/wiki/%F0%9F%94%97-%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%9E%E0%B8%B4%E0%B9%88%E0%B8%A1-%E0%B9%81%E0%B8%81%E0%B9%89%E0%B9%84%E0%B8%82-%E0%B8%81%E0%B8%A5%E0%B8%B8%E0%B9%88%E0%B8%A1%E0%B8%97%E0%B8%94%E0%B8%AA%E0%B8%AD%E0%B8%9A-%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88"


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
        raise Exception(f"Can't convert with any format...\n\n Num : {numResultData} \n\n Json...\n{JSONResultData}")

    # ? Check Data
    if not isinstance(usedData, dict):
        msg = f"Invalid subtask data...\nExpected Dict"
        printFail("SUBTASK", msg)
        raise Exception(msg)

    if "version" not in usedData:
        msg = f"Invalid subtask data...\nExpected 'version'"
        printFail("SUBTASK", msg)
        raise Exception(msg)

    if "data" not in usedData:
        msg = f"Invalid subtask data...\nExpected 'data'."
        printFail("SUBTASK", msg)
        raise Exception(msg)

    if not isinstance(usedData["data"], dict):
        msg = f"Invalid subtask data...\nExpected Dict in 'Data'"
        printFail("SUBTASK", msg)
        raise Exception(msg)

    if len(usedData["data"]) == 0:
        msg = f"Invalid subtask data...\nNo subtask data? rlly?"
        printFail("SUBTASK", msg)
        raise Exception(msg)
    
    for subN in usedData["data"]:
        if not isinstance(usedData["data"][subN], dict):
            msg = f"Invalid subtask data...\nExpected Dict in {subN}"
            printFail("SUBTASK", msg)
            raise Exception(msg)

        if "case" not in usedData["data"][subN]:
            msg = f"Invalid subtask data...\nExpected case in {subN}"
            printFail("SUBTASK", msg)
            raise Exception(msg)

        if not isinstance(usedData["data"][subN]["case"], str):
            msg = f"Invalid subtask data...\nExpected 'string' case in {subN}"
            printFail("SUBTASK", msg)
            raise Exception(msg)

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
        msg = f"Invalid require data, Found loop in require"
        printFail("SUBTASK", msg)
        raise Exception(msg)

    if result.maxCase <= 0:
        msg = f"Invalid subtask data...\nNo case found (max case less than 1)"
        printFail("SUBTASK", msg)
        raise Exception(msg)

    return result


if __name__ == "__main__":

    bruhData = compile("""10""")
    print(bruhData)
    if not bruhData == None:
        for s in bruhData.subtasks:
            print(s)
