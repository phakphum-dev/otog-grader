import requests

from DTO.result import ResultDTO
from constants.osDotEnv import osEnv


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
    # TODO : Imprement memUse in DB
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
    requests.post(getUrl(f'result/{result.id}'), json=body)
