from datetime import datetime
import requests

from DTO.result import ResultDTO


def updateRunningInCase(resultId, case):
    requests.post(f'result/{resultId}/case', json={"case": case})


def updateResult(result: ResultDTO):
    # TODO : Imprement memUse in DB
    currentDate = datetime.now()
    status = "accept" if all(
        c in "P[]()" for c in result.result) or result.result == "Accepted" else "reject"
    body = {
        "result": result.result,
        "score": result.score,
        "timeUsed": result.sumTime,
        "memUsed": result.memUse,
        "status": status,
        "errmsg": result.errmsg,
        "updateDate": currentDate
    }
    requests.post(f'result/{result.id}', json=body)
