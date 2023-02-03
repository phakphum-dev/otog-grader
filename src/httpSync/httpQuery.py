import requests
import time

from DTO.result import ResultDTO
from constants.osDotEnv import osEnv
from message import *


def getUrl(path):
    return f'{osEnv.SYNC_HOST}:{osEnv.SYNC_PORT}/{path}'


def getTask():
    res = requests.get(getUrl('task'))
    if res.status_code == 200:
        return res.json()
    else:
        return None


def updateRunningInCase(resultId, case):
    # requests.post(getUrl(f'result/{resultId}/case'), json={"case": case})
    pass


def updateResult(result: ResultDTO):
    # TODO : Implement memUse in DB
    status = "accept" if all(
        c in "P[]()" for c in result.result) or result.result == "Accepted" else "reject"
    body = {
        "result": result.result,
        "score": result.score,
        "timeUsed": result.sumTime,
        "memUsed": result.memUse,
        "status": status,
        "errmsg": result.errmsg,
    }

    tries = 0
    while True:
        tries += 1
        if tries > 1:
            #? Don't print on first try
            printHeader("HTTP", f"Try to post back to grader ({tries} tries)")
        try:
            postResult = requests.post(
                getUrl(f'result/{result.id}'), json=body)
        except:
            printFail("HTTP", "Fail to Post... retrying")
            time.sleep(2)
            continue

        if postResult.status_code != 200:
            printFail(
                "HTTP", f"Fail to Post with code ({postResult.status_code})... retrying")
            time.sleep(2)
            continue
        else:
            printOKGreen("HTTP", "Posted and Done")
            break
